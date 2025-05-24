# 必要なパッケージをインストール
from requirements import install_required_packages
from logger import print_log
install_required_packages()

import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv
from datetime import datetime
import logging

# discord.pyのログを完全に無効化
logging.getLogger('discord').setLevel(logging.ERROR)
logging.getLogger('discord.client').setLevel(logging.ERROR)
logging.getLogger('discord.gateway').setLevel(logging.ERROR)
logging.getLogger('discord.http').setLevel(logging.ERROR)

# .envファイルから環境変数を読み込む
load_dotenv()

def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print_log('config.jsonが見つかりません。デフォルト設定を使用します。', "WARNING")
        return {
            'prefix': '!',
            'welcome_message': 'ようこそ！',
            'welcome_enabled': True,
            'status_type': 'online',
            'status_message': '',
            'commands': [],
            'triggers': []
        }

# ボットの設定
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

config = load_config()
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

def replace_variables(message, user, guild):
    """メッセージ内の変数を置換する"""
    return message.replace('{user}', user.mention) \
                 .replace('{username}', user.name) \
                 .replace('{server}', guild.name)

# コマンドを動的に追加
for cmd in config.get('commands', []):
    @bot.command(name=cmd['name'])
    async def command(ctx, *, args=None):
        # コマンド名から対応する応答を探す
        command_name = ctx.command.name
        for cmd in config['commands']:
            if cmd['name'] == command_name:
                print_log(f'コマンド実行: {ctx.author} が {config["prefix"]}{command_name} を実行', "COMMAND")
                response = replace_variables(cmd['response'], ctx.author, ctx.guild)
                await ctx.send(response)
                break

@bot.event
async def on_ready():
    print_log(f'{bot.user} としてログインしました', "BOT")
    print_log(f'プレフィックス: {config["prefix"]}', "CONFIG")

    # ステータスの設定
    status_type = getattr(discord.Status, config.get('status_type', 'online'))
    activity = discord.Game(name=config.get('status_message', '')) if config.get('status_message') else None
    await bot.change_presence(status=status_type, activity=activity)
    print_log(f'ステータス: {config["status_type"]} - {config["status_message"] or "なし"}', "CONFIG")

    if config.get('commands'):
        print_log('登録されているコマンド:', "COMMANDS")
        for cmd in config['commands']:
            print_log(f'  - {config["prefix"]}{cmd["name"]}: {cmd["response"]}', "COMMAND")

    if config.get('triggers'):
        print_log('登録されているメッセージトリガー:', "TRIGGERS")
        for trigger in config['triggers']:
            match_type = "部分一致" if trigger['match_type'] == 'partial' else "完全一致"
            print_log(f'  - トリガー: {trigger["text"]} ({match_type})', "TRIGGER")
            print_log(f'    応答: {trigger["response"]}', "RESPONSE")

@bot.event
async def on_member_join(member):
    if config.get('welcome_enabled', True):
        channel = member.guild.system_channel
        if channel:
            welcome_message = replace_variables(config['welcome_message'], member, member.guild)
            print_log(f'ウェルカムメッセージ: {member} が参加しました', "WELCOME")
            await channel.send(f"{member.mention} {welcome_message}")

@bot.event
async def on_message(message):
    # ボット自身のメッセージは無視
    if message.author == bot.user:
        return

    # トリガーのチェック
    for trigger in config.get('triggers', []):
        if trigger['match_type'] == 'exact' and message.content == trigger['text']:
            print_log(f'トリガー実行: {message.author} が "{trigger["text"]}" を送信 (完全一致)', "TRIGGER")
            response = replace_variables(trigger['response'], message.author, message.guild)
            await message.channel.send(response)
            return
        elif trigger['match_type'] == 'partial' and trigger['text'] in message.content:
            print_log(f'トリガー実行: {message.author} が "{trigger["text"]}" を含むメッセージを送信 (部分一致)', "TRIGGER")
            response = replace_variables(trigger['response'], message.author, message.guild)
            await message.channel.send(response)
            return

    # コマンドの処理を続行
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print_log(f'存在しないコマンドが実行されました: {ctx.author} が {ctx.message.content} を実行', "ERROR")
        await ctx.send("そのコマンドは存在しません。")
    else:
        print_log(f'エラーが発生しました: {error}', "ERROR")

# ボットを起動
print_log('ボットを起動しています...', "STARTUP")
try:
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print_log('エラー: DISCORD_TOKENが設定されていません。.envファイルを確認してください。', "ERROR")
        print_log('1. .envファイルが存在することを確認してください。', "ERROR")
        print_log('2. .envファイルに DISCORD_TOKEN=あなたのトークン が正しく設定されているか確認してください。', "ERROR")
        exit(1)
    bot.run(token)
except discord.errors.LoginFailure:
    print_log('エラー: トークンが無効です。以下の点を確認してください：', "ERROR")
    print_log('1. トークンが正しくコピーされているか確認してください。', "ERROR")
    print_log('2. トークンが有効期限切れになっていないか確認してください。', "ERROR")
    print_log('3. ボットのトークンが正しいか確認してください。', "ERROR")
    exit(1)
except Exception as e:
    print_log(f'予期せぬエラーが発生しました: {str(e)}', "ERROR")
    exit(1)
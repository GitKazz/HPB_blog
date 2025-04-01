import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini APIの設定
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')

def analyze_image(image_path):
    """
    画像を分析し、特徴と説明文を生成する
    """
    try:
        # 画像を読み込む
        img = Image.open(image_path)
        
        # 特徴抽出用のプロンプト
        feature_prompt = """
        以下の画像のヘアスタイルを、ホットペッパービューティーでよく使われるような一言で表現してください。
        制約：
        - 15文字以内
        - ヘアスタイルの特徴を日本語で簡潔に
        例：「韓国風レイヤーカット」「前髪ありミディアム」など
        """
        
        # 説明文生成用のプロンプト
        description_prompt = """
        以下の画像を見て、美容師がブログに書くような「スタイルの解説文」を200文字程度で日本語で作ってください。
        例：「顔周りにしっかりレイヤーを入れ、韓国風の大人かわいい印象に仕上げました。○○な方にもおすすめです。」など
        """
        
        # 特徴の生成
        feature_response = model.generate_content([feature_prompt, img])
        feature = feature_response.text.strip()
        
        # 説明文の生成
        description_response = model.generate_content([description_prompt, img])
        description = description_response.text.strip()
        
        return {
            'feature': feature,
            'description': description
        }
        
    except Exception as e:
        raise Exception(f"画像分析中にエラーが発生しました: {str(e)}") 
#!/bin/bash

# GCPプロジェクトIDを設定（実際のプロジェクトIDに変更してください）
PROJECT_ID="dify-seo-api-2025"
SERVICE_NAME="seo-fastapi"
REGION="asia-northeast1"

echo "=== GCP Cloud Run デプロイスクリプト ==="
echo "プロジェクトID: $PROJECT_ID"
echo "サービス名: $SERVICE_NAME"
echo "リージョン: $REGION"
echo ""

# 1. プロジェクトを設定
echo "1. GCPプロジェクトを設定中..."
gcloud config set project $PROJECT_ID

# 2. 必要なAPIを有効化
echo "2. 必要なAPIを有効化中..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# 3. Cloud Buildでビルド・デプロイ
echo "3. Cloud Buildでビルド・デプロイ中..."
gcloud builds submit --config cloudbuild.yaml

# 4. デプロイされたURLを取得
echo "4. デプロイ完了！URLを取得中..."
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo ""
echo "=== デプロイ完了 ==="
echo "サービスURL: $SERVICE_URL"
echo "API仕様書: $SERVICE_URL/docs"
echo "ヘルスチェック: $SERVICE_URL/health"
echo ""
echo "Difyから呼び出す際のエンドポイント:"
echo "POST $SERVICE_URL/extract-headings"
echo ""
echo "テスト用curlコマンド:"
echo "curl -X POST \"$SERVICE_URL/extract-headings\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"urls\": [\"https://example.com/\"]}'"
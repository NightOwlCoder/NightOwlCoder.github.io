# Getting X (Twitter) API Credentials - Step by Step

## Step 1: Go to the Developer Portal

1. Open your browser and go to: **https://developer.twitter.com/en/portal/dashboard**
2. Log in with your @OwlCoder Twitter account
3. If prompted, apply for a developer account (it's free and usually approved instantly)

## Step 2: Create a New Project & App

1. Click **"+ Create Project"** (or use an existing one)
2. Give it a name like: `Blog Auto-Tweet`
3. Select use case: **"Making a bot"**
4. Provide a description: `Automatically tweets when new blog posts are published`
5. Click **"Next"** through the prompts

## Step 3: Create an App

1. Give your app a name: `nightowlcoder-blog-bot`
2. Click **"Complete"**

## Step 4: Get Your API Keys

You'll see your **API Key** and **API Key Secret** - SAVE THESE!

1. Copy the **API Key** somewhere safe
2. Copy the **API Key Secret** somewhere safe
3. Click **"Yes, I saved them"**

## Step 5: Enable Write Permissions

1. In your app dashboard, click **"Settings"**
2. Scroll to **"User authentication settings"**
3. Click **"Set up"**
4. Under **"App permissions"**, select **"Read and Write"**
5. Fill in required fields:
   - **Type of App**: Web App
   - **Callback URI**: `https://nightowlcoder.github.io/`
   - **Website URL**: `https://nightowlcoder.github.io/`
6. Click **"Save"**

## Step 6: Generate Access Tokens

1. Go to the **"Keys and tokens"** tab
2. Under **"Access Token and Secret"**, click **"Generate"**
3. Copy these values:
   - **Access Token**
   - **Access Token Secret**

## ✅ You should now have 4 values:

1. ✓ API Key (Consumer Key)
2. ✓ API Key Secret (Consumer Secret)  
3. ✓ Access Token
4. ✓ Access Token Secret

**Keep these safe!** We'll add them to GitHub in the next step.

---

**Once you have all 4 values, let me know and I'll set up the GitHub Action!**

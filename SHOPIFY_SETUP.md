# Shopify Integration Setup Guide

This guide will help you connect your Shopify store to the Evaly Product Analyzer.

## Prerequisites

- A Shopify store (any plan)
- Admin access to your Shopify store
- Basic understanding of API credentials

## Step 1: Create a Custom App in Shopify

1. **Log into your Shopify Admin Panel**
   - Go to your store admin: `https://your-store.myshopify.com/admin`

2. **Navigate to Apps**
   - Click on **Settings** (bottom left)
   - Click on **Apps and sales channels**
   - Click on **Develop apps** button

3. **Enable Custom App Development** (if not already enabled)
   - Click **Allow custom app development**
   - Read the warning and click **Allow custom app development** again

4. **Create a New App**
   - Click **Create an app** button
   - Enter an app name: `Evaly Product Analyzer`
   - Select an App developer (usually yourself)
   - Click **Create app**

## Step 2: Configure Admin API Access

1. **Configure Admin API scopes**
   - Click on **Configure Admin API scopes**
   - Select the following permissions:
     - `read_products` (required)
     - `read_inventory` (optional, for stock info)
     - `read_product_listings` (optional)
   - Click **Save**

2. **Install the App**
   - Click on the **API credentials** tab
   - Click **Install app**
   - Confirm by clicking **Install**

## Step 3: Get Your API Credentials

1. **Reveal Your Admin API Access Token**
   - After installation, you'll see **Admin API access token**
   - Click **Reveal token once**
   - **IMPORTANT**: Copy this token immediately and save it securely
   - You won't be able to see it again!

2. **Note Your Store URL**
   - Your store URL format: `your-store-name.myshopify.com`
   - Don't include `https://` - just the domain

## Step 4: Connect to Evaly

1. **Run the Evaly app**
   ```bash
   streamlit run app.py
   ```

2. **In the sidebar**
   - Check the box: **Connect to Shopify Store**
   - Enter your **Store URL**: `your-store-name.myshopify.com`
   - Enter your **Admin API Token**: (paste the token from Step 3)
   - Click **Test Connection**

3. **If successful**
   - You'll see: ✅ Connected to [Your Store Name]
   - You can now fetch products from your store!

## Using Shopify Products in Analysis

1. **Expand "Load Product from Shopify"**
2. **Click "Fetch Products"** - loads up to 50 products
3. **Select a product** from the dropdown
4. **Product details auto-fill** in the analysis form
5. **Adjust cost/price** if needed
6. **Run analysis** as usual!

## Troubleshooting

### "Failed to connect" Error
- Double-check your store URL format (no https://, just the domain)
- Verify your API token is correct
- Ensure the custom app is installed
- Check that `read_products` permission is enabled

### "Error fetching products" Error
- Verify your store has products
- Check API permissions include `read_products`
- Try reinstalling the custom app

### Import Errors
- Make sure you've installed requirements:
  ```bash
  pip install -r requirements.txt
  ```

## Security Notes

- **Never commit your API token** to version control
- Store your token in environment variables for production
- Regularly rotate your API tokens
- Only grant necessary permissions
- Disable/delete unused custom apps

## API Rate Limits

- Shopify has rate limits on API calls
- Default: 2 requests per second
- The app fetches 50 products at a time
- For large catalogs, products are limited to most recent 50

## Need Help?

- [Shopify API Documentation](https://shopify.dev/docs/api/admin-rest)
- [Custom Apps Guide](https://help.shopify.com/en/manual/apps/custom-apps)
- [API Access Scopes](https://shopify.dev/docs/api/usage/access-scopes)

---

**Ready to analyze your products?** Follow the steps above and start making data-driven decisions! 🚀

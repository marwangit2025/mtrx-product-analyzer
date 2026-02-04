"""
Shopify API Connector Module
Handles authentication and product fetching from Shopify stores
"""

import shopify
import requests
from typing import List, Dict, Optional


class ShopifyConnector:
    """
    Connector class for Shopify API integration
    Supports both Admin API and REST API methods
    """

    def __init__(self, shop_url: str, access_token: str):
        """
        Initialize Shopify connection

        Args:
            shop_url: Your Shopify store URL (e.g., 'mystore.myshopify.com')
            access_token: Admin API access token
        """
        self.shop_url = shop_url.replace('https://', '').replace('http://', '')
        if not self.shop_url.endswith('.myshopify.com'):
            if '.' not in self.shop_url:
                self.shop_url = f"{self.shop_url}.myshopify.com"

        self.access_token = access_token
        self.api_version = '2024-01'
        self.session = None

    def connect(self) -> bool:
        """
        Establish connection to Shopify store

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Create a new session
            self.session = shopify.Session(
                self.shop_url,
                self.api_version,
                self.access_token
            )
            shopify.ShopifyResource.activate_session(self.session)

            # Test connection by fetching shop info
            shop = shopify.Shop.current()
            return True
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False

    def get_products(self, limit: int = 50) -> List[Dict]:
        """
        Fetch products from Shopify store

        Args:
            limit: Maximum number of products to fetch (default: 50)

        Returns:
            List of product dictionaries
        """
        try:
            products = []
            shopify_products = shopify.Product.find(limit=limit)

            for product in shopify_products:
                # Get the first variant for pricing
                variant = product.variants[0] if product.variants else None

                product_data = {
                    'id': product.id,
                    'name': product.title,
                    'price': float(variant.price) if variant else 0.0,
                    'compare_at_price': float(variant.compare_at_price) if variant and variant.compare_at_price else None,
                    'sku': variant.sku if variant else '',
                    'inventory_quantity': variant.inventory_quantity if variant else 0,
                    'product_type': product.product_type,
                    'vendor': product.vendor,
                    'tags': product.tags,
                    'status': product.status,
                    'created_at': str(product.created_at),
                    'image_url': product.images[0].src if product.images else None,
                    'variants_count': len(product.variants),
                    'handle': product.handle,
                    'url': f"https://{self.shop_url}/products/{product.handle}"
                }

                products.append(product_data)

            return products

        except Exception as e:
            print(f"Error fetching products: {str(e)}")
            return []

    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """
        Fetch a single product by ID

        Args:
            product_id: Shopify product ID

        Returns:
            Product dictionary or None
        """
        try:
            product = shopify.Product.find(product_id)
            variant = product.variants[0] if product.variants else None

            return {
                'id': product.id,
                'name': product.title,
                'price': float(variant.price) if variant else 0.0,
                'compare_at_price': float(variant.compare_at_price) if variant and variant.compare_at_price else None,
                'sku': variant.sku if variant else '',
                'inventory_quantity': variant.inventory_quantity if variant else 0,
                'product_type': product.product_type,
                'vendor': product.vendor,
                'tags': product.tags,
                'status': product.status,
                'created_at': str(product.created_at),
                'image_url': product.images[0].src if product.images else None,
                'variants_count': len(product.variants),
                'handle': product.handle,
                'url': f"https://{self.shop_url}/products/{product.handle}"
            }

        except Exception as e:
            print(f"Error fetching product: {str(e)}")
            return None

    def search_products(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Search products by title

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of matching product dictionaries
        """
        try:
            products = shopify.Product.find(title=query, limit=limit)
            result = []

            for product in products:
                variant = product.variants[0] if product.variants else None
                result.append({
                    'id': product.id,
                    'name': product.title,
                    'price': float(variant.price) if variant else 0.0,
                    'sku': variant.sku if variant else '',
                    'vendor': product.vendor,
                    'status': product.status
                })

            return result

        except Exception as e:
            print(f"Error searching products: {str(e)}")
            return []

    def get_shop_info(self) -> Optional[Dict]:
        """
        Get basic shop information

        Returns:
            Shop info dictionary or None
        """
        try:
            shop = shopify.Shop.current()
            return {
                'name': shop.name,
                'email': shop.email,
                'domain': shop.domain,
                'currency': shop.currency,
                'timezone': shop.timezone,
                'plan_name': shop.plan_name
            }
        except Exception as e:
            print(f"Error fetching shop info: {str(e)}")
            return None

    def disconnect(self):
        """
        Close Shopify session
        """
        if self.session:
            shopify.ShopifyResource.clear_session()
            self.session = None


def test_connection(shop_url: str, access_token: str) -> tuple[bool, str]:
    """
    Test Shopify connection with provided credentials

    Args:
        shop_url: Shopify store URL
        access_token: Admin API access token

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        connector = ShopifyConnector(shop_url, access_token)
        if connector.connect():
            shop_info = connector.get_shop_info()
            connector.disconnect()

            if shop_info:
                return True, f"✅ Connected to {shop_info['name']}"
            else:
                return True, "✅ Connection successful"
        else:
            return False, "❌ Failed to connect. Check your credentials."

    except Exception as e:
        return False, f"❌ Connection error: {str(e)}"

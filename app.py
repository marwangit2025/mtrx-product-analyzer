import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

# ==========================================
# PART 1: THE EVALY INTELLIGENCE ENGINE
# ==========================================

class EvalyEngine:
    def __init__(self, product_data, api_key, model_provider="OpenAI"):
        self.data = product_data
        self.model_type = product_data['business_model']
        self.platform = product_data['platform']
        self.provider = model_provider
        
        # --- THE MODEL ROUTER ---
        # This switches brains based on user selection
        if self.provider == "OpenAI (GPT-4o)":
            self.llm = ChatOpenAI(
                temperature=0.0, 
                model="gpt-4o", 
                api_key=api_key
            )
        elif self.provider == "Google (Gemini 1.5 Pro)":
            self.llm = ChatGoogleGenerativeAI(
                temperature=0.0, 
                model="gemini-1.5-pro", 
                google_api_key=api_key
            )
        elif self.provider == "Anthropic (Claude 3.5 Sonnet)":
            self.llm = ChatAnthropic(
                temperature=0.0, 
                model="claude-3-5-sonnet-20240620", 
                api_key=api_key
            )
        else:
            # Fallback
            self.llm = ChatOpenAI(temperature=0.0, model="gpt-4o", api_key=api_key)

    def run_analysis(self):
        # 1. The Master Prompt
        context_prompt = ChatPromptTemplate.from_template(
            """
            You are the Evaly Intelligence Engine. Analyze this product for the {model} business model on {platform}.
            
            Product: {product_name}
            Price: {price}
            Cost: {cost}
            
            Perform a deep 9-point analysis.
            
            1. Profit Margin: Calculate Net Margin after fees (Estimate FBA/TikTok fees if applicable).
            
            2. Platform Fit & Native Ad Potential: 
               - Is this product native to {platform}? (e.g. Visual for TikTok, Search-heavy for Amazon).
               - **Native/Image Ad Suitability:** Does this product work for Native Advertising (Taboola/Outbrain) or Image Advertising (Pinterest/Instagram)? 
               - Does it have a "weird" or "shocking" visual that stops the scroll in a news feed?
            
            3. Trend Velocity: Is this trending up, down, or flat?
            4. Competition: Estimate saturation level.
            
            5. Content Difficulty (THE VIRAL TEST): 
               Evaluate the product against these 4 specific 'Viral' questions. If the answer to any is 'No', lower the score significantly:
               - Can I show a clear before and after in under 10 seconds?
               - Does the product solve a problem people already know they have?
               - Can I demonstrate 3-5 different use cases without losing clarity?
               - Would someone understand what this does if they saw it used once with zero explanation?
               
            6. Shipping Risk: Breakage/Returns/Weight.
            7. Scalability: Can this go to $100k/month?
            8. Brand Potential: Can we build a moat?
            9. Risk Factors: IP, Liability, Seasonality.

            Output a JSON with scores (0-100) for each, a short reasoning, and a Final Verdict:
            - GREENLIGHT (Perfect)
            - GO (Good, proceed)
            - FIX (Good but needs tweaks)
            - KILL (Do not touch)
            
            {format_instructions}
            """
        )
        
        # Define the JSON structure for the AI to fill out
        response_schemas = [
            ResponseSchema(name="verdict", description="GREENLIGHT, GO, FIX, or KILL"),
            ResponseSchema(name="action_plan", description="3 bullet points on what to do next"),
            ResponseSchema(name="scores", description="JSON object with keys: margin, platform_fit, trend, competition, content, shipping, scalability, brand, risk. Each has 'score' (0-10) and 'insight' (string).")
        ]
        
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()
        
        msg = context_prompt.format_messages(
            model=self.model_type,
            platform=self.platform,
            product_name=self.data['name'],
            price=self.data['price'],
            cost=self.data['cost'],
            format_instructions=format_instructions
        )
        
        response = self.llm.invoke(msg)
        return output_parser.parse(response.content)

def analyze_product(input_data, api_key, model_provider):
    engine = EvalyEngine(input_data, api_key, model_provider)
    return engine.run_analysis()


# ==========================================
# PART 2: THE STREAMLIT DASHBOARD (UI)
# ==========================================

# Page Config
st.set_page_config(page_title="Evaly - Multi-Model Intelligence", layout="wide", page_icon="⚡")

# Custom CSS for the SaaS look
st.markdown("""
<style>
    .stMetric {background-color: #f0f2f6; padding: 10px; border-radius: 5px;}
    .big-font {font-size:24px !important; font-weight: bold;}
    .verdict-box {padding: 20px; border-radius: 10px; text-align: center; color: white; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: BRAIN SELECTION ---
with st.sidebar:
    st.title("⚡ EVALY PRO")
    st.markdown("### 🧠 Select Your Brain")
    
    model_choice = st.selectbox(
        "Choose AI Model", 
        ["OpenAI (GPT-4o)", "Google (Gemini 1.5 Pro)", "Anthropic (Claude 3.5 Sonnet)"]
    )
    
    st.divider()
    
    # Dynamic Key Input based on selection
    user_api_key = ""
    if model_choice == "OpenAI (GPT-4o)":
        user_api_key = st.text_input("OpenAI API Key", type="password")
        st.caption("Best for: Logic & Reasoning")
        
    elif model_choice == "Google (Gemini 1.5 Pro)":
        user_api_key = st.text_input("Google Gemini API Key", type="password")
        st.caption("Best for: Large Context & Speed")
        
    elif model_choice == "Anthropic (Claude 3.5 Sonnet)":
        user_api_key = st.text_input("Anthropic API Key", type="password")
        st.caption("Best for: Nuance & Creative Angles")

    st.divider()
    st.info("**Supported Models:**\n- Dropshipping\n- Amazon FBA\n- TikTok Shop\n- Private Label\n- Wholesale")

# --- MAIN APP ---
st.title(f"⚡ Evaly Product Intelligence")

# STEP 1: CONTEXT
col1, col2 = st.columns(2)
with col1:
    biz_model = st.selectbox("1. Choose Business Model", 
        ["Dropshipping", "Amazon FBA", "TikTok Shop", "Private Label", "Wholesale/B2B"])
with col2:
    platform = st.selectbox("2. Select Platform", 
        ["Shopify", "Amazon", "TikTok Shop", "Etsy", "WooCommerce", "Native Ads (Taboola/Outbrain)"])

# STEP 2: PRODUCT DETAILS
with st.expander("3. Enter Product Details", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        p_name = st.text_input("Product Name / URL", "Example: Red Light Therapy Belt")
    with c2:
        cost = st.number_input("Landed Cost (COGS + Shipping)", 0.0, value=28.0)
        price = st.number_input("Target Sale Price", 0.0, value=129.0)
    with c3:
        # Just a visual element for the user
        st.selectbox("Risk Tolerance / Budget", ["Low (<$500)", "Medium ($1k-$5k)", "High ($10k+)"])
        
    start_btn = st.button("🚀 RUN EVALY ANALYSIS", type="primary", use_container_width=True)

# STEP 3: RESULTS
if start_btn:
    if not user_api_key:
        st.error(f"Please enter your {model_choice} API Key in the sidebar.")
    else:
        with st.spinner(f"🤖 {model_choice} is running the 9-Point Analysis..."):
            
            # Prepare Data
            input_data = {
                "name": p_name,
                "cost": cost,
                "price": price,
                "business_model": biz_model,
                "platform": platform
            }
            
            try:
                # Run Engine
                result = analyze_product(input_data, user_api_key, model_choice)
                scores = result['scores']
                
                # --- VERDICT HEADER ---
                verdict = result['verdict']
                color = "#28a745" if verdict in ["GREENLIGHT", "GO"] else "#dc3545" # Green or Red
                if verdict == "FIX": color = "#ffc107" # Yellow
                
                st.markdown(f"""
                <div style="background-color: {color};" class="verdict-box">
                    <h1 style="margin:0; color:white;">VERDICT: {verdict}</h1>
                    <p>{result['action_plan'][0]}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.divider()
                
                # --- THE 9-POINT SCORECARD ---
                st.subheader("📊 The 9-Point Scorecard")
                
                # Row 1
                r1c1, r1c2, r1c3 = st.columns(3)
                with r1c1:
                    st.metric("💰 Profit Margin", f"{scores['margin']['score']}/10", help=scores['margin']['insight'])
                    st.caption(scores['margin']['insight'])
                with r1c2:
                    st.metric("🛒 Platform Fit", f"{scores['platform_fit']['score']}/10", help=scores['platform_fit']['insight'])
                    st.caption(scores['platform_fit']['insight'])
                with r1c3:
                    st.metric("📈 Trend Velocity", f"{scores['trend']['score']}/10", help=scores['trend']['insight'])
                    st.caption(scores['trend']['insight'])
                    
                st.divider()
                
                # Row 2
                r2c1, r2c2, r2c3 = st.columns(3)
                with r2c1:
                    st.metric("⚔️ Competition", f"{scores['competition']['score']}/10", help=scores['competition']['insight'])
                    st.caption(scores['competition']['insight'])
                with r2c2:
                    st.metric("🎥 Content Difficulty", f"{scores['content']['score']}/10", help=scores['content']['insight'])
                    st.caption(scores['content']['insight'])
                with r2c3:
                    st.metric("📦 Shipping Risk", f"{scores['shipping']['score']}/10", help=scores['shipping']['insight'])
                    st.caption(scores['shipping']['insight'])

                st.divider()

                # Row 3
                r3c1, r3c2, r3c3 = st.columns(3)
                with r3c1:
                    st.metric("🚀 Scalability", f"{scores['scalability']['score']}/10", help=scores['scalability']['insight'])
                    st.caption(scores['scalability']['insight'])
                with r3c2:
                    st.metric("🏰 Brand Potential", f"{scores['brand']['score']}/10", help=scores['brand']['insight'])
                    st.caption(scores['brand']['insight'])
                with r3c3:
                    st.metric("⚠️ Risk Factors", f"{scores['risk']['score']}/10", help=scores['risk']['insight'])
                    st.caption(scores['risk']['insight'])

                # --- ACTION PLAN ---
                st.divider()
                st.subheader("📝 Action Plan")
                for item in result['action_plan']:
                    st.markdown(f"- {item}")
            
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.warning("Make sure your API Key is correct and has access to the selected model.")

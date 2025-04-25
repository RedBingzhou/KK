import streamlit as st
import numpy as np

# 页面配置
st.set_page_config(page_title="凯利指数计算器", layout="centered")
st.title("💰 凯利指数投注策略工具")
st.markdown("""
**公式**:  
`f = (b*p - q) / b`  
- `b`: 净赔率（赔率-1）  
- `p`: 预估胜率  
- `q`: 失败概率（1-p）  
""")

# 输入参数
with st.expander("⚙️ 输入参数", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        odds = st.number_input("赔率（例如2.5）", min_value=1.01, max_value=100.0, value=2.0)
    with col2:
        win_prob = st.number_input("预估胜率（%）", min_value=1, max_value=99, value=55) / 100
    with col3:
        bankroll = st.number_input("可用资金（元）", min_value=1, value=1000)

# 计算凯利指数
b = odds - 1  # 净赔率
q = 1 - win_prob

try:
    kelly_fraction = (b * win_prob - q) / b
except ZeroDivisionError:
    st.error("赔率不能为1")
    st.stop()

# 结果展示
if kelly_fraction > 0:
    # 安全限制：最多建议投入25%的资金
    safe_fraction = min(kelly_fraction, 0.25)
    suggested_bet = safe_fraction * bankroll

    col1, col2 = st.columns(2)
    with col1:
        st.metric("理论凯利比例", f"{kelly_fraction*100:.1f}%")
    with col2:
        st.metric("安全投注比例", f"{safe_fraction*100:.1f}%", delta="风险控制上限25%")
    
    st.success(f"✅ 建议投注金额: **{suggested_bet:.0f}元**")
    
    # 风险提示
    if kelly_fraction > 0.25:
        st.warning("⚠️ 理论比例过高，已自动限制为25%以保证资金安全")
else:
    st.error("❌ 凯利指数≤0：不应进行本次投注")

# 附加说明
st.divider()
st.markdown("""
**使用说明**  
1. **赔率**：指净赔率（例如赔率2.0 = 1:1回报）  
2. **预估胜率**：需独立于赔率评估（可通过历史数据分析）  
3. **安全限制**：防止单次投入过高（即使凯利公式建议更高）  
""")
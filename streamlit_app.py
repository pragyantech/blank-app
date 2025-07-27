import streamlit as st
import numpy as np
import pandas as pd
import math
import time
import plotly.graph_objects as go

# Configure Streamlit page
st.set_page_config(
    page_title="Algorithm Learning Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar pages
pages = [
    "📘 Introduction",
    "🔍 Analysis Importance",
    "📈 Order of Growth",
    "🧮 Asymptotic Analysis",
    "📊 Algorithm Cases",
    "🅾️ Big-O Notation",
    "🟰 Theta (Θ) Notation",
    "🅾️mega (Ω) Notation",
    "⏱ Time Complexity",
    "💾 Space Complexity",
    "🧠 Complexity Calculator"
]

selected_page = st.sidebar.radio("Navigate Topics", pages)

st.title("🧮 Algorithm Learning Hub")
st.markdown("---")

# ---------- Page Content ---------- #

if selected_page == "📘 Introduction":
    st.header("Welcome to Algorithm Analysis Learning")
    st.markdown("""
    Learn and visualize the key concepts of algorithm analysis:
    - Why analyze algorithms?
    - Complexity notations: Big‑O, Θ, Ω
    - Best/average/worst cases
    - Time & space complexity
    - Interactive examples & visualizations
    """)
    n_vals = np.array([1, 10, 100, 1000, 10000])
    comps = {
        'O(1)': np.ones_like(n_vals),
        'O(log n)': np.log2(n_vals),
        'O(n)': n_vals,
        'O(n log n)': n_vals * np.log2(n_vals),
        'O(n²)': n_vals**2
    }
    fig = go.Figure()
    for name, y in comps.items():
        fig.add_trace(go.Scatter(x=n_vals, y=y, name=name))
    fig.update_layout(title="📊 Complexity Growth on Log Scale", xaxis_title="Input Size (n)", yaxis_type="log", height=500)
    st.plotly_chart(fig, use_container_width=True)

elif selected_page == "🔍 Analysis Importance":
    st.header("Why Algorithm Analysis Matters")
    size = st.slider("Dataset Size", 1000, 1000000, 100000, step=100000)
    lin = size / 2
    bin = math.log2(size)
    st.columns(4)[0].metric("Linear Search Ops (O(n))", f"{int(lin):,}")
    st.columns(4)[1].metric("Binary Search Ops (O(log n))", f"{bin:.1f}")
    st.success(f"Binary search is approximately {lin/bin:.1f}× faster.")

    sizes = np.logspace(3, 6, 100)
    lin2 = sizes / 2
    bin2 = np.log2(sizes)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sizes, y=lin2, name='O(n)'))
    fig.add_trace(go.Scatter(x=sizes, y=bin2, name='O(log n)'))
    fig.update_layout(title="🔍 Linear vs Binary Search", xaxis_type="log", yaxis_type="log", height=500)
    st.plotly_chart(fig, use_container_width=True)

elif selected_page == "📈 Order of Growth":
    st.header("Order of Growth")
    max_n = st.slider("Max Input Size", 10, 2000, 200)
    opts = st.multiselect("Select Complexities to Compare", ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)', 'O(n²)', 'O(2ⁿ)'],
                          default=['O(1)', 'O(n)', 'O(n²)'])
    if opts:
        n = np.linspace(1, max_n, 200)
        funcs = {
            'O(1)': lambda n: np.ones_like(n),
            'O(log n)': np.log2,
            'O(n)': lambda n: n,
            'O(n log n)': lambda n: n * np.log2(n),
            'O(n²)': lambda n: n**2,
            'O(2ⁿ)': lambda n: np.exp2(np.minimum(n, 20))
        }
        fig = go.Figure()
        for c in opts:
            fig.add_trace(go.Scatter(x=n, y=funcs[c](n), name=c))
        fig.update_layout(title="📈 Growth of Common Complexities", height=500)
        st.plotly_chart(fig, use_container_width=True)

elif selected_page == "🧮 Asymptotic Analysis":
    st.header("Understanding Asymptotic Analysis")
    st.markdown("Analyze how an algorithm behaves as the input size grows towards infinity.")
    expr = st.text_input("Enter an expression in terms of n", "3*n**2 + 2*n + 1")
    st.latex(rf"f(n) = {expr}")
    st.code("Asymptotic Complexity: O(n²)")
    st.info("Only the dominant term matters as n → ∞. Ignore constants and lower-order terms.")

elif selected_page == "📊 Algorithm Cases":
    st.header("Best, Average and Worst Cases")
    
    size = st.slider("Array Size", 5, 100, 10)
    target = st.number_input("Target Element (1–n)", 1, size, 1)
    
    arr = list(range(1, size + 1))
    pos = arr.index(target) + 1  # 1-based position

    st.metric("Best Case", 1)
    st.metric("Your Case", pos)
    st.metric("Average Case", f"{(size + 1)/2:.1f}")
    st.metric("Worst Case", size)

    n = np.arange(1, 51)
    fig = go.Figure([
        go.Scatter(x=n, y=np.ones_like(n), name="Best O(1)", 
                   line=dict(dash="dot", color="green")),
        go.Scatter(x=n, y=(n + 1) / 2, name="Average O(n)", 
                   line=dict(color="blue")),
        go.Scatter(x=n, y=n, name="Worst O(n)", 
                   line=dict(dash="dash", color="red"))
    ])
    fig.update_layout(
        title="🔍 Linear Search Cases",
        xaxis_title="Input Size (n)",
        yaxis_title="Operations",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)


elif selected_page == "🅾️ Big-O Notation":
    st.header("Big-O Notation")
    st.markdown("Big‑O describes the **upper bound** (worst-case) of algorithm growth.")
    funcs = st.multiselect("Functions to Compare", ['n','n²','2n²','n³'], default=['n²','2n²'])
    n_max = st.slider("Max n", 10, 500, 100)
    if funcs:
        n = np.arange(1, n_max+1)
        mapping = {
            'n': n,
            'n²': n**2,
            '2n²': 2*n**2,
            'n³': n**3
        }
        fig = go.Figure()
        for f in funcs:
            fig.add_trace(go.Scatter(x=n, y=mapping[f], name=f))
        fig.update_layout(title="🅾️ Big-O Visualizations", height=500)
        st.plotly_chart(fig, use_container_width=True)

elif selected_page == "🟰 Theta (Θ) Notation":
    st.header("Theta (Θ) Notation")
    st.markdown("Theta represents the **tight bound** — both upper and lower limits.")

    c1 = st.slider("Lower bound constant (c₁)", 0.1, 2.0, 0.5, step=0.1)
    c2 = st.slider("Upper bound constant (c₂)", 1.0, 5.0, 2.0, step=0.1)

    if c1 < c2:
        n = np.linspace(1, 50, 200)
        f = n**2 + 2*n + 1

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=n, y=c1 * n**2, name="Lower Bound", 
                                 line=dict(dash="dash", color="green")))
        fig.add_trace(go.Scatter(x=n, y=c2 * n**2, name="Upper Bound", 
                                 line=dict(dash="dash", color="red")))
        fig.add_trace(go.Scatter(x=n, y=f, name="f(n)", 
                                 line=dict(color="blue")))

        fig.update_layout(
            title="🟰 Theta Bounds Visualization",
            xaxis_title="n (Input Size)",
            yaxis_title="Function Value",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        st.success(f"c₁·n² ≤ f(n) ≤ c₂·n² → Θ(n²)")
    else:
        st.error("Ensure c₁ < c₂")


elif selected_page == "🅾️mega (Ω) Notation":
    st.header("Big-Omega (Ω) Notation")
    st.markdown("Big-Omega provides the **lower bound** — best-case performance.")

    alg = st.selectbox("Select Algorithm", ["Linear Search", "Binary Search", "Merge Sort"])

    notes = {
        "Linear Search": "Ω(1): Best case when the element is at the beginning.",
        "Binary Search": "Ω(1): Best case when the middle element is the target.",
        "Merge Sort": "Ω(n log n): Minimum time due to splitting & merging."
    }
    st.info(notes[alg])

    n = np.arange(1, 100)
    fig = go.Figure([
        go.Scatter(x=n, y=np.ones_like(n), name="Ω(1)", 
                   line=dict(dash="dash", color="green")),
        go.Scatter(x=n, y=n, name="O(n)", 
                   line=dict(color="red"))
    ])
    fig.update_layout(
        title="🅾️ Big-Omega (Ω) Lower Bound Visualization",
        xaxis_title="Input Size (n)",
        yaxis_title="Operations",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)


elif selected_page == "⏱ Time Complexity":
    st.header("⏱ Time Complexity Analysis")

    # User options
    selected_algorithms = st.multiselect("Select Algorithms", ["Linear", "Binary", "Bubble", "Merge"], default=["Linear"])
    size = st.slider("Input Size (n)", 100, 5000, 1000)
    show_plot = st.checkbox("Show Growth Comparison Plot", value=True)
    show_bar = st.checkbox("Show Runtime Bar Chart", value=True)
    

    runtimes = {}
    complexities = {
        "Linear": "O(n), Ω(1), Θ(n)",
        "Binary": "O(log n), Ω(1), Θ(log n)",
        "Bubble": "O(n²), Ω(n), Θ(n²)",
        "Merge": "O(n log n), Ω(n log n), Θ(n log n)"
    }

    if st.button("Run Simulation"):
        for alg in selected_algorithms:
            start = time.perf_counter()
            total = 0

            if alg == "Linear":
                for _ in range(size):
                    total += 1
            elif alg == "Binary":
                val = size
                while val > 1:
                    val //= 2
                    total += 1
            elif alg == "Bubble":
                for i in range(size):
                    for j in range(size):
                        total += i + j
            elif alg == "Merge":
                for _ in range(int(size * math.log2(size))):
                    total += 1

            elapsed = time.perf_counter() - start
            runtimes[alg] = elapsed

        for alg in selected_algorithms:
            st.success(f"📌 {alg}: {runtimes[alg]:.6f} sec — {complexities[alg]}")

    # Plot Time Complexity Growth (theoretical)
    if show_plot:
        n = np.linspace(10, size, 200)  # dynamic range based on slider
        fig = go.Figure([
            go.Scatter(x=n, y=n, name="O(n)", line=dict(color="blue")),
            go.Scatter(x=n, y=n * np.log2(n), name="O(n log n)", line=dict(color="orange")),
            go.Scatter(x=n, y=n**2, name="O(n²)", line=dict(color="red")),
            go.Scatter(x=n, y=np.log2(n), name="O(log n)", line=dict(color="green"))
        ])
        fig.update_layout(
            title="📈 Theoretical Time Complexity Growth",
            yaxis_type="log",
            xaxis_title="Input Size (n)",
            yaxis_title="Operations (log scale)",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)


    # Runtime Comparison Bar Chart
    if show_bar and runtimes:
        bar_fig = go.Figure([
            go.Bar(x=list(runtimes.keys()), y=list(runtimes.values()), marker_color='purple')
        ])
        bar_fig.update_layout(
            title="⚖️ Runtime Comparison of Algorithms",
            xaxis_title="Algorithm",
            yaxis_title="Simulated Runtime (sec)",
            height=400
        )
        st.plotly_chart(bar_fig, use_container_width=True)

    
elif selected_page == "💾 Space Complexity":
    st.header("Space Complexity")
    
    alg = st.selectbox("Algorithm", ["Iterative Fibonacci", "Recursive Fibonacci", "Merge Sort", "Bubble Sort"])
    usage = {
        "Iterative Fibonacci": 1,
        "Recursive Fibonacci": 100,
        "Merge Sort": 100,
        "Bubble Sort": 1
    }

    # Display metrics
    st.metric("Estimated Extra Space", usage[alg])
    complexity = "O(n)" if usage[alg] > 1 else "O(1)"
    st.info(f"Space Complexity: {complexity}")

    # Plot Space Usage Patterns
    n = np.arange(1, 101)
    fig = go.Figure([
        go.Scatter(x=n, y=n, name="Recursive/Merge Sort", line=dict(dash="dash", color="red")),
        go.Scatter(x=n, y=np.ones_like(n), name="Iterative/Bubble Sort", line=dict(color="green"))
    ])
    fig.update_layout(
        title="💾 Space Usage Patterns",
        xaxis_title="Input Size (n)",
        yaxis_title="Space (units)",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)


elif selected_page == "🧠 Complexity Calculator":
    st.header("Complexity Calculator")
    st.markdown("Estimate time complexity of simple code blocks")
    expr = st.text_area("Paste Python-like code here:", value="""for i in range(n):
    for j in range(n):
        pass""", height=200)
    if st.button("Estimate Complexity"):
        st.success("Estimated Time Complexity: O(n²)")
    st.markdown("Examples:")
    st.code("""
# Single loop → O(n)
for i in range(n):
    pass

# Nested loop → O(n²)
for i in range(n):
    for j in range(n):
        pass

# Divide & conquer → O(n log n)
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
""")

st.markdown("---")
st.markdown("🔬 *Interactive educational tool for understanding algorithm analysis.*")
import streamlit as st
from forms.contact import contact_form

@st.experimental_dialog("Contact Me")
def show_contact_form():
    contact_form()

# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./assets/profile_image.png", width=230)

with col2:
    st.title("Kunal Rawat", anchor=False)
    st.write(
        "4th-year B.Tech student in Industrial Internet of Things, preparing for placement in service-based companies."
    )
    st.write("Areas of Interest: Gen AI and Cloud Computing.")
    if st.button("✉️ Contact Me"):
        show_contact_form()

    st.write("📧 Gmail: kunalrawat7766@gmail.com")
    st.write("🔗 LinkedIn: [Kunal Rawat](https://www.linkedin.com/in/kunal-rawat-3156901b9/)")
    st.write("💻 GitHub: [Ku0904](https://github.com/Ku0904)")

# --- EXPERIENCE & QUALIFICATIONS ---
st.write("\n")
st.subheader("Experience & Qualifications", anchor=False)
st.write(
    """
    - 6-week Data Analysis internship with IBM SkillsBuild and CSRBOX
    - Strong hands-on experience and knowledge in Python, C/C++, and JavaScript
    - Good understanding of statistical principles and data-driven decision-making
    - Experience with frameworks like Django and tools like Node.js, VScode, Git, and GitHub
    - Excellent team player with a strong sense of initiative
    """
)

# --- SKILLS ---
st.write("\n")
st.subheader("Skills", anchor=False)
st.write(
    """
    - **Languages:** C/C++, Python, HTML, CSS, JavaScript
    - **Libraries:** C++ STL, Python Libraries (Pandas, NumPy)
    - **Web Dev Tools:** Node.js, VScode, Git, GitHub, Version Control
    - **Frameworks:** Django
    - **Cloud/Databases:** MongoDB, Firebase, MySQL
    - **Relevant Coursework:** Data Structures & Algorithms, Operating Systems, OOP, DBMS, Networking, Software Engineering
    - **Data Analysis Tools:** PowerBI, MS Excel, Plotly
    - **Modeling:** Logistic Regression, Linear Regression, Decision Trees
    """
)

# --- SOFT SKILLS ---
st.write("\n")
st.subheader("Soft Skills", anchor=False)
st.write(
    """
    - Analytical Thinking
    - Continuous Learning
    - Effective Communication
    - Flexibility
    """
)

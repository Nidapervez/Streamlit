import streamlit as st
import pandas as pd
import os
import random
import json

# Constants
POSTS_FILE = "posts.json"
AVATAR_URLS = [
    "https://i.pravatar.cc/40?img=1", "https://i.pravatar.cc/40?img=2", 
    "https://i.pravatar.cc/40?img=3", "https://i.pravatar.cc/40?img=4"
]

# Load existing posts
def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "r") as f:
            return json.load(f)
    return []

# Save posts
def save_posts(posts):
    with open(POSTS_FILE, "w") as f:
        json.dump(posts, f, indent=4)

# Create post
def create_post(title, content, image_url):
    posts = load_posts()
    posts.append({
        "id": len(posts) + 1,
        "title": title,
        "content": content,
        "image": image_url,
        "likes": 0,
        "comments": []
    })
    save_posts(posts)
    st.success("✅ Post Created Successfully!")

# Add comment
def add_comment(post_id, comment):
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            post["comments"].append({
                "text": comment,
                "avatar": random.choice(AVATAR_URLS)  # Random avatar for user
            })
            break
    save_posts(posts)
    st.success("💬 Comment Added!")

# Like a post
def like_post(post_id):
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            post["likes"] += 1
            break
    save_posts(posts)

# Custom Styles
st.markdown("""
    <style>
        .stApp { background-color: #121212; color: #E0E0E0; }
        .title { text-align: center; font-size: 2.5rem; color: #00BFFF; text-shadow: 2px 2px 4px rgba(0, 191, 255, 0.5); }
        .card { background-color: #1E1E1E; padding: 20px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0px 4px 10px rgba(255, 64, 129, 0.2); }
        .comment { background-color: #222; padding: 10px; border-radius: 8px; margin: 8px 0; }
        .comment-avatar { border-radius: 50%; margin-right: 10px; }
        .comment-text { display: flex; align-items: center; }
        .stButton > button { background-color: #00BFFF !important; color: white; border-radius: 8px; padding: 8px 15px; font-weight: bold; }
        .stButton > button:hover { background-color: #FF4081 !important; }
    </style>
""", unsafe_allow_html=True)

# UI
st.markdown("<h1 class='title'>📝 Social Post & Review App</h1>", unsafe_allow_html=True)
tabs = st.tabs(["📌 Create Post", "📜 View Posts"])

with tabs[0]:  # Create Post
    st.subheader("📝 Create a New Post")
    title = st.text_input("Post Title")
    content = st.text_area("Post Content")
    image = st.text_input("Post Image URL (Optional)")
    if st.button("Publish Post"):
        if title and content:
            create_post(title, content, image)
        else:
            st.warning("⚠️ Please enter title and content.")

with tabs[1]:  # View Posts
    st.subheader("📜 All Posts")
    posts = load_posts()

    if posts:
        for post in posts[::-1]:  # Show latest posts first
            st.markdown(f"""
                <div class="card">
                    <h3 style="color:#00BFFF;">📌 {post['title']}</h3>
                    <p>{post['content']}</p>
                    {"<img src='" + post['image'] + "' width='100%' style='border-radius: 10px;'/>" if post['image'] else ""}
                    <p style="color: #FF4081;">❤️ {post['likes']} Likes</p>
                </div>
            """, unsafe_allow_html=True)

            # Like Button
            if st.button(f"👍 Like {post['title']}", key=f"like_{post['id']}"):
                like_post(post["id"])
                st.rerun()

            # Display Comments
            st.markdown("💬 **Comments:**")
            for comment in post["comments"]:
                st.markdown(f"""
                    <div class="comment">
                        <div class="comment-text">
                            <img class="comment-avatar" src="{comment['avatar']}" width="30"/>
                            {comment['text']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # Add Comment
            new_comment = st.text_input(f"💭 Add Comment on '{post['title']}'", key=f"comment_{post['id']}")
            if st.button(f"Submit Comment on '{post['title']}'", key=f"submit_comment_{post['id']}"):
                if new_comment:
                    add_comment(post["id"], new_comment)
                    st.rerun()
                else:
                    st.warning("⚠️ Please enter a comment.")
    else:
        st.write("No posts available. Create one first!")

st.success("✅ App Loaded Successfully!")

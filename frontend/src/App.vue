<template>
  <div class="app">
    <header class="app-header">
      <h1>ezblog Vue Editor</h1>
    </header>

    <main class="editor-layout">
      <section class="editor-pane">
        <h2 class="section-title">New Post</h2>
        <form class="post-form" @submit.prevent="handleCreatePost">
          <label class="field">
            <span class="field-label">Title</span>
            <input
              type="text"
              v-model="title"
              placeholder="Write a captivating title..."
            />
          </label>

          <label class="field">
            <span class="field-label">Content</span>
            <textarea
              v-model="content"
              placeholder="Start writing your post..."
              rows="8"
            ></textarea>
          </label>

          <button
            type="submit"
            class="primary-button"
            :disabled="submitting || !title.trim() || !content.trim()"
          >
            {{ submitting ? "Saving..." : "Create Post" }}
          </button>
        </form>
      </section>

      <section class="preview-pane">
        <h2 class="section-title">Posts</h2>

        <p v-if="error" class="error-text">{{ error }}</p>

        <p v-else-if="loading" class="muted-text">Loading posts...</p>
        <p v-else-if="posts.length === 0" class="muted-text">
          No posts yet. Create your first one!
        </p>
        <ul v-else class="post-list">
          <li v-for="post in posts" :key="post.id" class="post-item">
            <span class="post-title">{{ post.title }}</span>
            <button
              type="button"
              class="delete-button"
              @click="handleDeletePost(post.id)"
            >
              Delete
            </button>
          </li>
        </ul>
      </section>
    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

// Use environment variable for API URL, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const posts = ref([]);
const title = ref("");
const content = ref("");
const loading = ref(false);
const submitting = ref(false);
const error = ref("");

async function fetchPosts() {
  try {
    loading.value = true;
    error.value = "";
    const res = await fetch(`${API_BASE_URL}/posts`);
    if (!res.ok) {
      throw new Error("Failed to fetch posts");
    }
    const data = await res.json();
    posts.value = data;
  } catch (err) {
    error.value = err.message || "Unable to load posts";
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchPosts();
});

async function handleCreatePost() {
  if (!title.value.trim() || !content.value.trim()) return;

  try {
    submitting.value = true;
    error.value = "";
    const res = await fetch(`${API_BASE_URL}/posts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: title.value.trim(),
        content: content.value.trim(),
      }),
    });
    if (!res.ok) {
      throw new Error("Failed to create post");
    }
    const created = await res.json();
    posts.value = [created, ...posts.value];
    title.value = "";
    content.value = "";
  } catch (err) {
    error.value = err.message || "Unable to create post";
  } finally {
    submitting.value = false;
  }
}

async function handleDeletePost(id) {
  const original = [...posts.value];
  posts.value = posts.value.filter((post) => post.id !== id);

  try {
    error.value = "";
    const res = await fetch(`${API_BASE_URL}/posts/${id}`, {
      method: "DELETE",
    });
    if (!res.ok) {
      throw new Error("Failed to delete post");
    }
  } catch (err) {
    error.value = err.message || "Unable to delete post";
    posts.value = original; // revert on error
  }
}
</script>



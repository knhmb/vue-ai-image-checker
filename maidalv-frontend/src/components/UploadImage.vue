<template>
  <div>
    <h1>Upload Image</h1>
    <div class="upload-container">
      <input type="file" @change="onFileChange" />
      <button @click="uploadImage" :disabled="!image">Submit</button>
    </div>
    <p v-if="error" class="error-msg">{{ error }}</p>
    <div v-if="result" class="mt-4">
      <p><strong>Verdict:</strong> {{ result.verdict }}</p>
      <p><strong>Labels:</strong> {{ result.labels.join(', ') }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      image: null,
      result: null,
      error: '',
    }
  },
  methods: {
    onFileChange(e) {
      const file = e.target.files[0]
      this.error = ''
      this.result = null

      if (!file) return

      if (!file.type.startsWith('image/')) {
        this.error = 'Please upload a valid image file.'
        this.image = null
        return
      }

      this.image = file
    },
    async uploadImage() {
      const formData = new FormData()
      formData.append('image', this.image)

      try {
        const response = await fetch('http://localhost:5000/upload', {
          method: 'POST',
          body: formData,
        })

        const data = await response.json()
        console.log('data', data)

        this.result = data
      } catch (error) {
        console.error('Upload failed:', error)
      }
    },
  },
}
</script>

<style scoped>
.upload-container {
  display: flex;
}

.error-msg {
  color: red;
  font-size: 12px;
  margin: 0.5rem 0;
}
</style>

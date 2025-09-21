// GRADLINK Main JavaScript

document.addEventListener("DOMContentLoaded", () => {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map((tooltipTriggerEl) => new window.bootstrap.Tooltip(tooltipTriggerEl))

  // Initialize popovers
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  var popoverList = popoverTriggerList.map((popoverTriggerEl) => new window.bootstrap.Popover(popoverTriggerEl))

  // Auto-hide alerts after 5 seconds
  setTimeout(() => {
    var alerts = document.querySelectorAll(".alert")
    alerts.forEach((alert) => {
      var bsAlert = new window.bootstrap.Alert(alert)
      bsAlert.close()
    })
  }, 5000)

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })

  // Form validation enhancement
  const forms = document.querySelectorAll(".needs-validation")
  forms.forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }
      form.classList.add("was-validated")
    })
  })

  // Search functionality
  const searchInput = document.getElementById("searchInput")
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const searchTerm = this.value.toLowerCase()
      const searchableItems = document.querySelectorAll(".searchable-item")

      searchableItems.forEach((item) => {
        const text = item.textContent.toLowerCase()
        if (text.includes(searchTerm)) {
          item.style.display = ""
        } else {
          item.style.display = "none"
        }
      })
    })
  }

  // Like button functionality
  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("like-btn")) {
      e.preventDefault()
      const btn = e.target
      const postId = btn.dataset.postId

      fetch(`/community/like/${postId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            const icon = btn.querySelector("i")
            const count = btn.querySelector(".like-count")

            if (data.liked) {
              icon.classList.remove("far")
              icon.classList.add("fas")
              btn.classList.add("text-danger")
            } else {
              icon.classList.remove("fas")
              icon.classList.add("far")
              btn.classList.remove("text-danger")
            }

            count.textContent = data.like_count
          }
        })
        .catch((error) => console.error("Error:", error))
    }
  })

  // Connection request functionality
  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("connect-btn")) {
      e.preventDefault()
      const btn = e.target
      const userId = btn.dataset.userId

      fetch(`/alumni/connect/${userId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            btn.textContent = "Request Sent"
            btn.classList.remove("btn-success")
            btn.classList.add("btn-secondary")
            btn.disabled = true
          }
        })
        .catch((error) => console.error("Error:", error))
    }
  })

  // Image preview for file uploads
  const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]')
  imageInputs.forEach((input) => {
    input.addEventListener("change", (e) => {
      const file = e.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          const preview = document.getElementById("imagePreview")
          if (preview) {
            preview.src = e.target.result
            preview.style.display = "block"
          }
        }
        reader.readAsDataURL(file)
      }
    })
  })

  // Infinite scroll for feeds
  let loading = false
  const page = 1

  function loadMoreContent() {
    if (loading) return
    loading = true

    const loadMoreBtn = document.getElementById("loadMoreBtn")
    if (loadMoreBtn) {
      loadMoreBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...'
    }

    // Implement your load more logic here
    setTimeout(() => {
      loading = false
      if (loadMoreBtn) {
        loadMoreBtn.innerHTML = "Load More"
      }
    }, 1000)
  }

  // Load more button click handler
  const loadMoreBtn = document.getElementById("loadMoreBtn")
  if (loadMoreBtn) {
    loadMoreBtn.addEventListener("click", loadMoreContent)
  }

  // Auto-scroll to load more content
  window.addEventListener("scroll", () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
      const feedContainer = document.getElementById("feedContainer")
      if (feedContainer && !loading) {
        loadMoreContent()
      }
    }
  })
})

// Utility function to get CSRF token
function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// Show loading spinner
function showLoading(element) {
  element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...'
  element.disabled = true
}

// Hide loading spinner
function hideLoading(element, originalText) {
  element.innerHTML = originalText
  element.disabled = false
}

// Show toast notification
function showToast(message, type = "success") {
  const toastContainer = document.getElementById("toastContainer")
  if (!toastContainer) {
    const container = document.createElement("div")
    container.id = "toastContainer"
    container.className = "toast-container position-fixed top-0 end-0 p-3"
    document.body.appendChild(container)
  }

  const toast = document.createElement("div")
  toast.className = `toast align-items-center text-white bg-${type} border-0`
  toast.setAttribute("role", "alert")
  toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `

  document.getElementById("toastContainer").appendChild(toast)
  const bsToast = new window.bootstrap.Toast(toast)
  bsToast.show()

  toast.addEventListener("hidden.bs.toast", () => {
    toast.remove()
  })
}

// Format date
function formatDate(dateString) {
  const options = { year: "numeric", month: "short", day: "numeric" }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

// Debounce function for search
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

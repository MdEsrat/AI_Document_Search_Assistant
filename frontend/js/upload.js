// Upload functionality
const API_BASE_URL = '/api';

const uploadForm = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const progressContainer = document.getElementById('progressContainer');
const alertContainer = document.getElementById('alertContainer');
const documentsList = document.getElementById('documentsList');

// Upload form submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const file = fileInput.files[0];
    if (!file) {
        showAlert('Please select a file', 'danger');
        return;
    }
    
    if (!file.name.endsWith('.pdf')) {
        showAlert('Only PDF files are allowed', 'danger');
        return;
    }
    
    await uploadDocument(file);
});

// Upload document
async function uploadDocument(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Show progress
    progressContainer.classList.remove('d-none');
    uploadBtn.disabled = true;
    alertContainer.innerHTML = '';
    
    try {
        const response = await fetch(`${API_BASE_URL}/documents/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert(
                `Success! ${data.filename} uploaded and processed. Created ${data.num_chunks} chunks.`,
                'success'
            );
            fileInput.value = '';
            loadDocuments();
        } else {
            // Show the specific error message from the server
            showAlert(data.message || 'Upload failed', 'danger');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showAlert('Network error uploading document. Please check if the server is running.', 'danger');
    } finally {
        progressContainer.classList.add('d-none');
        uploadBtn.disabled = false;
    }
}

// Load documents list
async function loadDocuments() {
    try {
        const response = await fetch(`${API_BASE_URL}/documents/`);
        const data = await response.json();
        
        if (data.documents && data.documents.length > 0) {
            displayDocuments(data.documents);
        } else {
            documentsList.innerHTML = '<p class="text-muted">No documents uploaded yet.</p>';
        }
    } catch (error) {
        console.error('Error loading documents:', error);
        documentsList.innerHTML = '<p class="text-danger">Error loading documents.</p>';
    }
}

// Display documents
function displayDocuments(documents) {
    const html = documents.map(doc => `
        <div class="document-item">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h6 class="mb-1">
                        <i class="bi bi-file-earmark-pdf text-danger"></i>
                        ${doc.filename}
                    </h6>
                    <small class="text-muted">
                        Uploaded: ${new Date(doc.upload_date).toLocaleString()} | 
                        Chunks: ${doc.num_chunks} | 
                        Size: ${formatFileSize(doc.file_size)}
                    </small>
                </div>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteDocument('${doc.id}', '${doc.filename}')">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
    
    documentsList.innerHTML = html;
}

// Delete document
async function deleteDocument(docId, filename) {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/documents/${docId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showAlert(`Document "${filename}" deleted successfully`, 'success');
            loadDocuments();
        } else {
            showAlert('Error deleting document', 'danger');
        }
    } catch (error) {
        console.error('Delete error:', error);
        showAlert('Error deleting document', 'danger');
    }
}

// Show alert message
function showAlert(message, type) {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    alertContainer.innerHTML = alertHtml;
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Load documents on page load
loadDocuments();

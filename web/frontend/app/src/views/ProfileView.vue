<script setup lang="ts">
import { ref, computed } from 'vue';
import { Pencil } from 'lucide-vue-next';
import { useCurrentUser } from '@/composables/useCurrentUser';
import accountIcon from '@/assets/account-icon.svg';

const { currentUser } = useCurrentUser();

// Local editable state
const editableUsername = ref('');
const companyDescription = ref('');
const imageFile = ref<File | null>(null);
const imagePreview = ref<string>('');
const currentPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const isEditing = ref(false);

// Initialize editable username when currentUser is available
const initializeForm = () => {
  if (currentUser.value) {
    editableUsername.value = currentUser.value.username;
    // Set default profile image
    imagePreview.value = accountIcon;
  }
};

// Initialize form when component mounts or user changes
if (currentUser.value) {
  initializeForm();
}

// Computed property to check if passwords are valid
const isPasswordValid = computed(() => {
  if (!newPassword.value) return true; // No password change
  return newPassword.value === confirmPassword.value && newPassword.value.length >= 8;
});

// Computed property to check if save button should be enabled
const canSave = computed(() => {
  if (!editableUsername.value.trim()) return false;
  if (newPassword.value && !isPasswordValid.value) return false;
  return true;
});

// Handle image file selection
const handleImageSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  
  if (file) {
    imageFile.value = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.value = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  }
};

// Trigger file input click
const triggerImageUpload = () => {
  const fileInput = document.getElementById('image-upload') as HTMLInputElement;
  fileInput?.click();
};

// Placeholder function for updating profile
const handleSave = async () => {
  if (!canSave.value) return;
  
  // TODO: Implement API call to update user profile
  console.log('Saving user profile...');
  console.log('Username:', editableUsername.value);
  console.log('Company Description:', companyDescription.value);
  console.log('Image file:', imageFile.value);
  console.log('Password change requested:', !!newPassword.value);
  
  // Simulate API call
  alert('Profile update functionality will be implemented when API is ready');
  
  // Reset password fields after save
  currentPassword.value = '';
  newPassword.value = '';
  confirmPassword.value = '';
  isEditing.value = false;
};
</script>

<template>
    <main>
        <h2>User Profile</h2>
        <div v-if="currentUser" class="profile-container">
            <!-- Profile Image Section -->
            <div class="profile-image-section">
                <div class="image-container">
                    <img :src="imagePreview" alt="Profile" class="profile-image" />
                    <button class="edit-image-btn" @click="triggerImageUpload" type="button">
                        <Pencil :size="20" />
                    </button>
                    <input 
                        type="file" 
                        id="image-upload" 
                        accept="image/*" 
                        @change="handleImageSelect"
                        style="display: none"
                    />
                </div>
            </div>

            <!-- Profile Form -->
            <form @submit.prevent="handleSave" class="profile-form">
                <!-- Username Section -->
                <div class="form-group">
                    <label for="username">Username</label>
                    <div class="input-wrapper input-gradient-border">
                        <input 
                            type="text" 
                            id="username" 
                            v-model="editableUsername"
                            required
                            class="form-input styled-input"
                        />
                    </div>
                </div>

                <!-- Company Description Section -->
                <div class="form-group">
                    <label for="company-description">Company Description</label>
                    <div class="input-wrapper input-gradient-border">
                        <textarea 
                            id="company-description" 
                            v-model="companyDescription"
                            class="form-input form-textarea styled-input"
                            rows="4"
                            placeholder="Enter your company description..."
                        ></textarea>
                    </div>
                </div>

                <!-- Change Password Section -->
                <div class="password-section">
                    <h3>Change Password</h3>
                    
                    <div class="password-fields">
                        <div class="form-group">
                            <label for="current-password">Current Password</label>
                            <div class="input-wrapper input-gradient-border">
                                <input 
                                    type="password" 
                                    id="current-password" 
                                    v-model="currentPassword"
                                    class="form-input styled-input"
                                    autocomplete="current-password"
                                />
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="new-password">New Password</label>
                            <div class="input-wrapper input-gradient-border">
                                <input 
                                    type="password" 
                                    id="new-password" 
                                    v-model="newPassword"
                                    class="form-input styled-input"
                                    autocomplete="new-password"
                                    placeholder="Leave blank to keep current"
                                />
                            </div>
                            <small v-if="newPassword && newPassword.length < 8" class="error-text">
                                Password must be at least 8 characters
                            </small>
                        </div>

                        <div class="form-group">
                            <label for="confirm-password">Confirm New Password</label>
                            <div class="input-wrapper input-gradient-border">
                                <input 
                                    type="password" 
                                    id="confirm-password" 
                                    v-model="confirmPassword"
                                    class="form-input styled-input"
                                    autocomplete="new-password"
                                />
                            </div>
                            <small v-if="newPassword && confirmPassword && newPassword !== confirmPassword" class="error-text">
                                Passwords do not match
                            </small>
                        </div>
                    </div>
                </div>
                <!-- Save Button: moved up to reduce wasted space -->
                <div class="form-actions">
                    <button 
                        type="submit" 
                        class="gradient-button"
                        :disabled="!canSave"
                    >
                        Save Changes
                    </button>
                </div>
            </form>
        </div>
        <div v-else class="loading">
            <p>Loading user profile...</p>
        </div>
    </main>
</template>

<style scoped>
main {
    padding: 1.5rem;
    max-width: 1400px;
    margin: 0 auto;
    height: calc(100vh - 3rem);
    display: flex;
    flex-direction: column;
}

h2 {
    margin-bottom: 1rem;
    color: var(--color-heading);
    font-size: 1.5rem;
}

.profile-container {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 1.5rem;
    align-items: start;
    flex: 1;
    min-height: 0;
}

/* Profile Image Section */
.profile-image-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1.5rem;
    background-color: var(--color-background-soft);
    border-radius: 8px;
    border: 1px solid var(--color-border);
    height: fit-content;
}

.image-container {
    position: relative;
    width: 160px;
    height: 160px;
}

.profile-image {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--color-border);
}

.edit-image-btn {
    position: absolute;
    bottom: 5px;
    right: 5px;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: var(--color-background);
    border: 2px solid var(--color-border);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px var(--shadow-color);
}

@media (hover: hover) {
    .edit-image-btn:hover {
        filter: brightness(0.5);
    }
}

@media (prefers-color-scheme: dark) {
    @media (hover: hover) {
        .edit-image-btn:hover {
            filter: brightness(1.5);
        }
    }
}

.edit-image-btn svg {
    color: var(--color-text);
}

/* Profile Form */
.profile-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    background-color: var(--color-background-soft);
    padding: 1.5rem;
    border-radius: 8px;
    border: 1px solid var(--color-border);
    height: auto;
    overflow-y: visible;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
}

.form-group label {
    font-weight: 600;
    color: var(--color-text);
    font-size: 0.9rem;
}

.form-input {
    padding: 0.6rem;
    border: 1px solid var(--color-border);
    border-radius: 8px;
    font-size: 0.95rem;
    font-family: inherit;
    transition: border-color 0.2s ease;
    background-color: var(--color-background);
    color: var(--color-text);
}

.form-input:focus {
    outline: none;
    border-color: var(--color-border-hover);
}

.form-textarea {
    resize: none;
    min-height: 80px;
    max-height: 120px;
    line-height: 1.4;
    font-family: inherit;
}

/* Password Section */
.password-section {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
    padding-top: 0.8rem;
    border-top: 1px solid var(--color-border);
}

.password-section h3 {
    margin: 0;
    color: var(--color-heading);
    font-size: 1rem;
}

.password-fields {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}

.error-text {
    color: var(--color-threat);
    font-size: 0.8rem;
}

/* Form Actions */
.form-actions {
    display: flex;
    justify-content: flex-end;
    padding-top: 0.5rem;
}

.loading {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 400px;
    color: var(--color-text-muted);
}

/* Responsive Design */
@media (max-width: 1400px) {
    .password-fields {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 1024px) {
    .profile-container {
        grid-template-columns: 250px 1fr;
        gap: 1.5rem;
    }
    
    .image-container {
        width: 140px;
        height: 140px;
    }
    
    .password-fields {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    main {
        padding: 1rem;
        height: auto;
    }
    
    .profile-container {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }
    
    .profile-image-section {
        padding: 1.5rem;
    }
    
    .image-container {
        width: 120px;
        height: 120px;
    }
    
    .password-fields {
        grid-template-columns: 1fr;
    }
    
    .profile-form {
        height: auto;
    }
}

/* Ensure gradient border pseudo-element is visible above the form background
   (the global utils.css uses z-index: -1 which can be hidden by parent backgrounds)
*/
.input-wrapper.input-gradient-border {
    position: relative;
    z-index: 0;
}
.input-wrapper.input-gradient-border::before {
    z-index: 0; /* bring gradient above parent backgrounds */
}
.input-wrapper.input-gradient-border .styled-input {
    position: relative;
    z-index: 1; /* keep input above the gradient so text is interactive */
    -webkit-background-clip: padding-box;
    background-clip: padding-box;
}
</style>
<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { Pencil, Trash2 } from 'lucide-vue-next';
import ConfirmModal from '@/components/ConfirmModal.vue';
import { useCurrentUser } from '@/composables/useCurrentUser';
import accountIcon from '@/assets/account-icon.svg';
import type { UserUpdateData } from '@/types';
import router from '@/router';

const { currentUser, fetchUser } = useCurrentUser();

// Local editable state
const editableUsername = ref('');
const companyDescription = ref('');
const imageFile = ref<File | null>(null);
const imagePreview = ref<string>('');
const imageRemoveRequested = ref(false);
const currentPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const isEditing = ref(false);
// For account deletion
const deletePassword = ref('');
const deleteError = ref('');
const isDeleting = ref(false);
const showDeleteConfirm = ref(false);

// Snapshot of original values to detect unsaved changes
const originalUser = ref({
    username: '',
    companyDescription: '',
    imagePreview: '',
});

// Initialize editable username when currentUser is available
const initializeForm = () => {
    if (currentUser.value) {
        editableUsername.value = currentUser.value.username;
        companyDescription.value = currentUser.value.companyDescription;
        // Set default profile image
        imagePreview.value = accountIcon;
        originalUser.value.imagePreview = imagePreview.value;
        fetch('/api/me/picture', {
            method: 'GET',
            credentials: 'include',
        }).then((response) => {
            if (response.ok) {
                return response.blob();
            } else {
                throw new Error('No profile picture');
            }
        }).then((blob) => {
            imagePreview.value = URL.createObjectURL(blob);
            originalUser.value.imagePreview = imagePreview.value;
        }).catch(() => {
            // Use default icon if no picture
            imagePreview.value = accountIcon;
        });
        imageRemoveRequested.value = false;

        // Save original snapshot for dirty-checking
        originalUser.value.username = editableUsername.value;
        originalUser.value.companyDescription = companyDescription.value;
    }
};

// Initialize form when component mounts or user changes
if (currentUser.value) {
    initializeForm();
}

// Also re-initialize when the current user changes
watch(currentUser, (newVal) => {
    if (newVal) initializeForm();
});

onMounted(() => {
    if (currentUser.value) initializeForm();
});

// Computed property to check if passwords are valid
const isPasswordValid = computed(() => {
    if (!newPassword.value) return true; // No password change
    return newPassword.value === confirmPassword.value;
});

// Whether the current preview represents the default image
const isDefaultImage = computed(() => {
    // treat either the bundled svg or the API endpoint as the default
    return (
        imagePreview.value === accountIcon ||
        imagePreview.value === '/api/me/picture' ||
        !imagePreview.value
    );
});

// Computed property to check if save button should be enabled
const canSave = computed(() => {
    // Require username and password validity when changing password
    if (!editableUsername.value.trim()) return false;
    if (newPassword.value && !isPasswordValid.value) return false;
    // Only allow save when something changed
    return isDirty.value;
});

// Dirty-check: compare current editable values against original snapshot
const isDirty = computed(() => {
    if (!originalUser.value) return false;
    if (editableUsername.value !== originalUser.value.username) return true;
    if (companyDescription.value !== originalUser.value.companyDescription) return true;
    if (imageFile.value) return true; // new image selected
    if (imageRemoveRequested.value) return true; // removal requested
    if (imagePreview.value !== originalUser.value.imagePreview) return true;
    if (newPassword.value) return true; // password change requested
    return false;
});

// Handle image file selection
const handleImageSelect = (event: Event) => {
    const target = event.target as HTMLInputElement;
    const file = target.files?.[0];
    
    if (file) {
        imageFile.value = file;
        // If user selects a new file, they no longer request removal
        imageRemoveRequested.value = false;
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

// Mark profile picture for removal — actual DELETE happens on Save
const removeProfilePicture = () => {
    // If there's a selected file, clear it (user intends to remove instead)
    imageFile.value = null;
    imageRemoveRequested.value = true;
    // Show client-side default so user sees the change
    imagePreview.value = accountIcon;
    console.log('Profile picture removal requested (will be sent on save)');
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
    
    // If user requested picture removal, perform DELETE on save
    if (imageRemoveRequested.value) {
        try {
            await fetch('/api/me/picture', {
                method: 'DELETE',
                credentials: 'include',
            });
            console.log('Profile picture removed on save');
        } catch (error) {
            console.error('Error removing profile picture on save:', error);
        }
    }

    if (imageFile.value) {
        const formData = new FormData();
        formData.append("picture", imageFile.value);
        fetch("/api/me/picture", {
            method: "POST",
            credentials: "include",
            body: formData
        }).then(() => {
            console.log("Profile picture updated");
        }).catch((error) => {
            console.error("Error updating profile picture:", error);
        });
    }

    const updateData: UserUpdateData = {
        username: editableUsername.value,
        companyDescription: companyDescription.value,
        password: currentPassword.value ? currentPassword.value : undefined,
        newPassword: newPassword.value ? newPassword.value : undefined,
    }
    fetch("/api/me", {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(updateData),
    }).then(() => {
        console.log("User profile updated");
        fetchUser();
    }).catch((error) => {
        console.error("Error updating user profile:", error);
    });

    // On success: update original snapshot so form is considered saved
    originalUser.value.username = editableUsername.value;
    originalUser.value.companyDescription = companyDescription.value;
    originalUser.value.imagePreview = imagePreview.value;

    // Reset temporary fields
    currentPassword.value = '';
    newPassword.value = '';
    confirmPassword.value = '';
    imageFile.value = null;
    imageRemoveRequested.value = false;
    isEditing.value = false;
};

// Allow discarding local edits and restoring original snapshot
const discardChanges = () => {
    editableUsername.value = originalUser.value.username;
    companyDescription.value = originalUser.value.companyDescription;
    imagePreview.value = originalUser.value.imagePreview;
    imageFile.value = null;
    imageRemoveRequested.value = false;
    currentPassword.value = '';
    newPassword.value = '';
    confirmPassword.value = '';
    // reset delete fields as well
    deletePassword.value = '';
    deleteError.value = '';
};

// Handle account deletion
const handleDeleteAccount = async () => {
    deleteError.value = '';
    if (!deletePassword.value) {
        deleteError.value = 'Please provide your password to delete your account.';
        return;
    }

    // confirmation is handled by the modal; this function performs the deletion
    isDeleting.value = true;
    try {
        const body = {
            password: deletePassword.value,
        };

        const res = await fetch('/api/me', {
            method: 'DELETE',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });

        if (res.ok) {
            console.log(await res.json());
            // close modal and update UI
            showDeleteConfirm.value = false;
            await fetchUser();
            router.push('/login');
        } else {
            console.error('Delete account failed');
            deleteError.value = 'Failed to delete account.';
        }
    } catch (err) {
        deleteError.value = 'Network error while deleting account.';
        console.error('Error deleting account:', err);
    } finally {
        isDeleting.value = false;
    }
};
</script>

<template>
    <main>
        <h2>User Profile</h2>
        <!-- Unsaved changes indicator -->
        <Transition name="dirty-notification">
            <div v-if="isDirty" class="unsaved-indicator card gradient-background-light" role="status">
                <span class="unsaved-text">You have unsaved changes</span>
                <div class="unsaved-actions">
                    <button type="button" class="gradient-button" @click="handleSave" :disabled="!canSave">
                        Save
                    </button>
                    <button type="button" class="secondary-button" @click="discardChanges">
                        Discard
                    </button>
                </div>
            </div>
        </Transition>

        <div v-if="currentUser" class="profile-container">
            <!-- Profile Image Section -->
            <div class="profile-image-section">
                <div class="image-container">
                    <img :src="imagePreview" alt="Profile" class="profile-image" />
                    <button v-if="!isDefaultImage" class="edit-image-btn remove-image-btn" @click="removeProfilePicture" type="button" aria-label="Remove profile picture">
                        <Trash2 :size="18" />
                    </button>
                    <button class="edit-image-btn" @click="triggerImageUpload" type="button" aria-label="Edit profile picture">
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
                            <small v-else-if="newPassword && confirmPassword === ''" class="error-text">
                                Please confirm your new password
                            </small>
                        </div>
                    </div>
                </div>

                <!-- Delete Account Section -->
                <div class="danger-section">
                    <h3>Delete Account</h3>
                    <p class="danger-note">This action is permanent and will remove your account and data.</p>
                    <div class="form-group">
                        <label for="delete-password">Confirm with Password</label>
                        <div class="input-wrapper input-gradient-border">
                            <input
                                type="password"
                                id="delete-password"
                                v-model="deletePassword"
                                class="form-input styled-input"
                                placeholder="Enter your password to confirm"
                                autocomplete="current-password"
                            />
                        </div>
                        <small v-if="deleteError" class="error-text">{{ deleteError }}</small>
                    </div>

                    <div class="form-actions">
                        <button
                            type="button"
                            class="delete-button"
                            :disabled="!deletePassword || isDeleting"
                            @click="showDeleteConfirm = true"
                        >
                            {{ isDeleting ? 'Deleting...' : 'Delete Account' }}
                        </button>
                    </div>
                </div>
            </form>
            <ConfirmModal
                v-model:visible="showDeleteConfirm"
                title="Delete account?"
                :confirm-disabled="isDeleting || !deletePassword"
                confirmText="Delete"
                cancelText="Cancel"
                :error="deleteError"
                @confirm="handleDeleteAccount"
            >
                <p>Are you sure you want to permanently delete your account? This action cannot be undone.</p>
            </ConfirmModal>
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
    display: flex;
    flex-direction: column;
}

h2 {
    margin-bottom: 1rem;
    color: var(--color-heading);
    font-size: 1.5rem;
}

/* Unsaved changes indicator - use site vars and utility classes */
.unsaved-indicator {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    background: var(--color-background-soft);
    border: 1px solid var(--color-border);
    color: var(--color-text);
    border-radius: 8px;
    margin: 0 0 1rem 0;
    padding: 0.5rem 0.75rem;
    /* Pin to bottom center of the viewport so the notification floats above content */
    position: fixed;
    left: 50%;
    transform: translateX(-50%);
    bottom: 1.25rem;
    z-index: 2200;
    max-width: calc(100% - 2rem);
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.12);
}

.unsaved-text {
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--color-text-opaque);
}
.unsaved-actions {
    display: flex;
    gap: 0.5rem;
}
/* make utility buttons fit the indicator */
.unsaved-actions .gradient-button,
.unsaved-actions .secondary-button {
    padding: 0.35rem 0.6rem;
    font-size: 0.9rem;
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

/* Remove button - same style as edit but positioned bottom-left */
.remove-image-btn {
    position: absolute;
    bottom: 5px;
    left: 5px;
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

/* Delete / danger section styles */
.danger-section {
    margin-top: 1.25rem;
    padding-top: 1rem;
    border-top: 1px solid var(--color-border);
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}
.danger-section .danger-note {
    color: var(--color-text-muted);
    font-size: 0.9rem;
    margin: 0;
}
.delete-button {
    background: var(--color-threat);
    color: var(--vt-c-white);
    border: none;
    padding: 0.55rem 0.9rem;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 700;
    transition: filter 0.2s ease;
}

@media (hover: hover) {
    .delete-button:hover:not(:disabled) {
        filter: brightness(0.8);
    }
}

@media (prefers-color-scheme: dark) {
    @media (hover: hover) {
        .delete-button:hover:not(:disabled) {
            filter: brightness(1.2);
        }
    }
}

.delete-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    background: var(--color-threat-light);
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
        margin-bottom: 6rem;
        height: auto;
        width: 100%;
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

    .unsaved-indicator {
        width: calc(100% - 2rem);
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

/* Modal styles moved to ConfirmModal.vue */

/* Transition for the dirty-notification Vue <Transition name="dirty-notification"> */
.dirty-notification-enter-from,
.dirty-notification-leave-to {
    opacity: 0;
    /* start slightly lower when animating in from the bottom */
    transform: translateY(8px);
}
.dirty-notification-enter-active,
.dirty-notification-leave-active {
    transition: opacity 220ms cubic-bezier(.2,.8,.2,1), transform 220ms cubic-bezier(.2,.8,.2,1);
}
.dirty-notification-enter-to,
.dirty-notification-leave-from {
    opacity: 1;
    transform: translateY(0);
}

/* Respect users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
    .dirty-notification-enter-active,
    .dirty-notification-leave-active {
        transition: none !important;
    }
}
</style>
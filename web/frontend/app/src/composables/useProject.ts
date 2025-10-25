import type { ProjectInDB } from "@/types";
import { ref } from "vue";

const project = ref<ProjectInDB | null>(null);
const projectId = ref<number | null>(null);
const isLoading = ref(false);
const error = ref<string | null>(null);

export function useProject() {
    async function fetchProject(_projectId: number): Promise<boolean> {
        projectId.value = _projectId;
        isLoading.value = true;
        error.value = null;

        try {
            const response = await fetch(`/api/projects/${_projectId}`, {
                credentials: "include",
            });

            if (response.ok) {
                const data: ProjectInDB = await response.json();
                project.value = data;
                return true;
            } else {
                project.value = null;
                return false;
            }
        } catch (err) {
            error.value = err instanceof Error ? err.message : "Unknown error";
            project.value = null;
            return false;
        } finally {
            isLoading.value = false;
        }
    }

    function clearProject() {
        project.value = null;
        error.value = null;
    }
 
    return {
        project,
        projectId,
        isLoading,
        error,
        fetchProject,
        clearProject,
    };
}
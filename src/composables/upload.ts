import type { FileData } from "~/types";

export const useUpload = () => {
  const fileData = ref<FileData>();

  const onDrop = async (files: File[] | null) => {
    if (!files) return;
    const file = files[0];
    const url = URL.createObjectURL(file);
    fileData.value = {
      name: file.name,
      url,
      type: file.type,
      lastModified: file.lastModified,
      file,
    };
  };

  const dropZoneRef = ref<HTMLElement>();

  const { isOverDropZone } = useDropZone(dropZoneRef, onDrop);

  const useInputEl = () => {
    const el = document.createElement("input");
    el.onchange = (e) => {
      const files = (e.target as HTMLInputElement).files as FileList;
      onDrop(Array.from(files));
    };
    el.setAttribute("type", "file");
    el.setAttribute("multiple", "false");
    el.setAttribute("accept", "image/*");
    el.click();
  };

  return {
    fileData,
    dropZoneRef,
    isOverDropZone,
    useInputEl,
  };
};

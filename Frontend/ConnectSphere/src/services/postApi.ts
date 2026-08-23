import api from "./api";

export const createPost = async (
  content: string,
  visibility: string = "PUBLIC",
  image?: File | null
) => {
  const formData = new FormData();

  formData.append("content", content);
  formData.append("visibility", visibility);

  if (image) {
    formData.append("images", image);
  }

  const response = await api.post(
    "/posts/create/",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};
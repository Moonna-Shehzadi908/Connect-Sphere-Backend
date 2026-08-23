import api from "./api";

export const getMyProfile = async () => {
  const response = await api.get("/profiles/me/");
  return response.data;
};

export const updateProfile = async (data: FormData) => {
  const response = await api.patch(
    "/profiles/me/update/",
    data,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const uploadAvatar = async (data: FormData) => {
  const response = await api.patch(
    "/profiles/me/avatar/",
    data,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const uploadCover = async (data: FormData) => {
  const response = await api.patch(
    "/profiles/me/cover/",
    data,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};
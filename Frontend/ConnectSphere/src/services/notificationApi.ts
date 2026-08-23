import api from "./api";


// =========================================================
// GET ALL NOTIFICATIONS
// =========================================================

export const getNotifications = async () => {
  const response = await api.get(
    "/notifications/"
  );

  return response.data;
};


// =========================================================
// GET UNREAD NOTIFICATION COUNT
// =========================================================

export const getUnreadNotificationCount = async () => {
  const response = await api.get(
    "/notifications/unread-count/"
  );

  return response.data;
};


// =========================================================
// MARK SINGLE NOTIFICATION AS READ
// =========================================================

export const markNotificationRead = async (
  notificationId: number
) => {
  const response = await api.patch(
    `/notifications/${notificationId}/read/`
  );

  return response.data;
};


// =========================================================
// MARK ALL NOTIFICATIONS AS READ
// =========================================================

export const markAllNotificationsRead = async () => {
  const response = await api.patch(
    "/notifications/read-all/"
  );

  return response.data;
};


// =========================================================
// DELETE NOTIFICATION
// =========================================================

export const deleteNotification = async (
  notificationId: number
) => {
  const response = await api.delete(
    `/notifications/${notificationId}/`
  );

  return response.data;
};
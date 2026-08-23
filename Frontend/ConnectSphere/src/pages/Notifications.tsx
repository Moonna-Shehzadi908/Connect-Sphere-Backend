import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  getNotifications,
  markNotificationRead,
  markAllNotificationsRead,
  deleteNotification,
} from "../services/notificationApi";

import "./Notifications.css";

interface Notification {
  id: number;
  message: string;
  notification_type?: string;
  is_read: boolean;
  created_at?: string;

  sender?: {
    id?: number;
    username?: string;
    avatar?: string;
  };
}

const Notifications = () => {
  const navigate = useNavigate();

  const [notifications, setNotifications] = useState<
    Notification[]
  >([]);

  const [loading, setLoading] = useState(true);

  // =========================================================
  // LOAD NOTIFICATIONS
  // =========================================================

  const loadNotifications = async () => {
    try {
      const data = await getNotifications();

      // Django REST Framework pagination:
      // { count, next, previous, results: [] }

      setNotifications(
        data.results || data || []
      );
    } catch (error) {
      console.error(
        "Failed to load notifications:",
        error
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadNotifications();
  }, []);

  // =========================================================
  // MARK SINGLE NOTIFICATION AS READ
  // =========================================================

  const handleMarkRead = async (
    id: number
  ) => {
    try {
      await markNotificationRead(id);

      setNotifications((prev) =>
        prev.map((notification) =>
          notification.id === id
            ? {
                ...notification,
                is_read: true,
              }
            : notification
        )
      );
    } catch (error) {
      console.error(
        "Failed to mark notification as read:",
        error
      );
    }
  };

  // =========================================================
  // MARK ALL NOTIFICATIONS AS READ
  // =========================================================

  const handleMarkAllRead = async () => {
    try {
      await markAllNotificationsRead();

      setNotifications((prev) =>
        prev.map((notification) => ({
          ...notification,
          is_read: true,
        }))
      );
    } catch (error) {
      console.error(
        "Failed to mark all notifications:",
        error
      );
    }
  };

  // =========================================================
  // DELETE NOTIFICATION
  // =========================================================

  const handleDelete = async (
    id: number
  ) => {
    try {
      await deleteNotification(id);

      setNotifications((prev) =>
        prev.filter(
          (notification) =>
            notification.id !== id
        )
      );
    } catch (error) {
      console.error(
        "Failed to delete notification:",
        error
      );
    }
  };

  // =========================================================
  // FORMAT DATE
  // =========================================================

  const formatDate = (
    date?: string
  ) => {
    if (!date) {
      return "";
    }

    return new Date(date).toLocaleString();
  };

  // =========================================================
  // GET NOTIFICATION ICON
  // =========================================================

  const getNotificationIcon = (
    notificationType?: string
  ) => {
    switch (notificationType) {
      case "LIKE":
        return "❤️";

      case "COMMENT":
        return "💬";

      case "FOLLOW":
        return "👤";

      case "MESSAGE":
        return "✉️";

      case "MODERATION_WARNING":
        return "⚠️";

      default:
        return "🔔";
    }
  };

  // =========================================================
  // GET NOTIFICATION TYPE LABEL
  // =========================================================

  const getNotificationLabel = (
    notificationType?: string
  ) => {
    switch (notificationType) {
      case "LIKE":
        return "Like";

      case "COMMENT":
        return "Comment";

      case "FOLLOW":
        return "Follow";

      case "MESSAGE":
        return "Message";

      case "MODERATION_WARNING":
        return "Moderation Warning";

      default:
        return "Notification";
    }
  };

  // =========================================================
  // RENDER
  // =========================================================

  return (
    <div className="notificationsPage">

      {/* =====================================================
          HEADER
      ====================================================== */}

      <div className="notificationsHeader">

        <div>
          <h1>
            Notifications
          </h1>

          <p>
            Stay updated with your latest activity
          </p>
        </div>

        <button
          className="markAllBtn"
          onClick={handleMarkAllRead}
        >
          Mark all as read
        </button>

      </div>

      {/* =====================================================
          NOTIFICATIONS LIST
      ====================================================== */}

      <div className="notificationsList">

        {loading ? (

          <div className="notificationEmpty">

            <p>
              Loading notifications...
            </p>

          </div>

        ) : notifications.length === 0 ? (

          <div className="notificationEmpty">

            <div className="emptyBell">
              🔔
            </div>

            <h3>
              No notifications yet
            </h3>

            <p>
              When someone interacts with your
              posts, you'll see notifications here.
            </p>

          </div>

        ) : (

          notifications.map(
            (notification) => {

              const isModerationWarning =
                notification.notification_type ===
                "MODERATION_WARNING";

              return (

                <div
                  key={notification.id}
                  className={`notificationCard ${
                    notification.is_read
                      ? "read"
                      : "unread"
                  } ${
                    isModerationWarning
                      ? "moderationWarning"
                      : ""
                  }`}
                >

                  {/* =================================================
                      ICON
                  ================================================== */}

                  <div className="notificationIcon">

                    {getNotificationIcon(
                      notification.notification_type
                    )}

                  </div>

                  {/* =================================================
                      CONTENT
                  ================================================== */}

                  <div className="notificationContent">

                    {/* Notification type */}

                    <small className="notificationType">

                      {getNotificationLabel(
                        notification.notification_type
                      )}

                    </small>

                    {/* Message */}

                    <div className="notificationMessage">

                      {notification.sender?.username && (

                        <strong>
                          {
                            notification.sender
                              .username
                          }
                        </strong>

                      )}

                      <span>
                        {notification.message}
                      </span>

                    </div>

                    {/* Date */}

                    {notification.created_at && (

                      <small>
                        {formatDate(
                          notification.created_at
                        )}
                      </small>

                    )}

                  </div>

                  {/* =================================================
                      ACTIONS
                  ================================================== */}

                  <div className="notificationActions">

                    {!notification.is_read && (

                      <button
                        className="readBtn"
                        onClick={() =>
                          handleMarkRead(
                            notification.id
                          )
                        }
                        title="Mark as read"
                      >
                        ✓
                      </button>

                    )}

                    <button
                      className="deleteBtn"
                      onClick={() =>
                        handleDelete(
                          notification.id
                        )
                      }
                      title="Delete notification"
                    >
                      🗑
                    </button>

                  </div>

                </div>

              );
            }
          )

        )}

      </div>

      {/* =====================================================
          BACK TO HOME FEED
      ====================================================== */}

      <button
        className="backNotificationsBtn"
        onClick={() =>
          navigate("/home")
        }
      >
        ← Back to Home
      </button>

    </div>
  );
};

export default Notifications;
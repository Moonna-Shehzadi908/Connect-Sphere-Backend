import { useEffect, useMemo, useRef, useState } from "react";
import "./MessagesPage.css";
import { useNavigate } from "react-router-dom";

import api from "../services/api";
import defaultProfile from "../assets/profile icone.webp";

interface ConnectUser {
  id: number;
  username: string;
  first_name?: string;
  last_name?: string;
  avatar?: string | null;
  profile?: {
    avatar?: string | null;
  };
}

interface Conversation {
  id: number;
  participant: ConnectUser | null;
  last_message: string;
  last_message_time: string | null;
  unread_count: number;
}

interface Message {
  id: number;
  content: string;
  sender: {
    id: number;
    username: string;
    avatar?: string | null;
  };
  attachment?: string | null;
  is_read: boolean;
  created_at: string;
}

const getMediaUrl = (value?: string | null) => {
  if (!value) return "";

  if (
    value.startsWith("http://") ||
    value.startsWith("https://")
  ) {
    return value;
  }

  return `http://127.0.0.1:8000${
    value.startsWith("/") ? value : `/${value}`
  }`;
};

const getAvatar = (
  user?: ConnectUser | Message["sender"] | null
) => {
  if (!user) return defaultProfile;

  const avatar =
    user.avatar ??
    ("profile" in user
      ? user.profile?.avatar
      : null);

  return avatar
    ? getMediaUrl(avatar)
    : defaultProfile;
};

const formatTime = (value?: string | null) => {
  if (!value) return "";

  return new Date(value).toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
  });
};

/*
 * Handles different DRF response formats safely.
 */
const getListData = (responseData: any): any[] => {
  if (Array.isArray(responseData)) {
    return responseData;
  }

  if (Array.isArray(responseData?.results)) {
    return responseData.results;
  }

  if (Array.isArray(responseData?.data)) {
    return responseData.data;
  }

  if (Array.isArray(responseData?.users)) {
    return responseData.users;
  }

  if (Array.isArray(responseData?.followers)) {
    return responseData.followers;
  }

  if (Array.isArray(responseData?.following)) {
    return responseData.following;
  }

  return [];
};

export default function MessagesPage() {
  /*
   * Current logged-in user is already stored in localStorage.
   * We do NOT call /profile/me/ because that endpoint does not
   * exist in the current backend.
   */
  const navigate = useNavigate();
  let currentUser: any = {};

  try {
    currentUser = JSON.parse(
      localStorage.getItem("user") || "{}"
    );
  } catch {
    currentUser = {};
  }

  const currentUserId = Number(currentUser?.id || 0);
  const currentUsername = currentUser?.username || "";

  const [conversations, setConversations] = useState<
    Conversation[]
  >([]);

  const [messages, setMessages] = useState<Message[]>([]);

  const [connections, setConnections] = useState<
    ConnectUser[]
  >([]);

  const [
    selectedConversationId,
    setSelectedConversationId,
  ] = useState<number | null>(null);

  const [
    selectedParticipant,
    setSelectedParticipant,
  ] = useState<ConnectUser | null>(null);

  const [messageText, setMessageText] = useState("");

  const [searchText, setSearchText] = useState("");

  const [userSearchText, setUserSearchText] =
    useState("");

  const [attachment, setAttachment] =
    useState<File | null>(null);

  const [
    showNewConversation,
    setShowNewConversation,
  ] = useState(false);

  const [
    showEmojiPicker,
    setShowEmojiPicker,
  ] = useState(false);

  const [
    loadingConversations,
    setLoadingConversations,
  ] = useState(true);

  const [
    loadingMessages,
    setLoadingMessages,
  ] = useState(false);

  const [sending, setSending] = useState(false);

  const [loadingUsers, setLoadingUsers] =
    useState(false);

  const [error, setError] = useState("");

  const fileInputRef =
    useRef<HTMLInputElement>(null);

  const messagesEndRef =
    useRef<HTMLDivElement>(null);

  /*
   * Merge users from followers/following and
   * conversation participants.
   */
  const userMap = useMemo(() => {
    const map = new Map<number, ConnectUser>();

    connections.forEach((person) => {
      map.set(person.id, person);
    });

    conversations.forEach((conversation) => {
      const person = conversation.participant;

      if (person?.id) {
        const old = map.get(person.id);

        map.set(person.id, {
          ...old,
          ...person,
          avatar:
            person.avatar ||
            person.profile?.avatar ||
            old?.avatar ||
            old?.profile?.avatar ||
            null,
        });
      }
    });

    return map;
  }, [connections, conversations]);

  const emojis = [
    "😀",
    "😃",
    "😄",
    "😁",
    "😆",
    "😅",
    "😂",
    "🤣",
    "😊",
    "😇",
    "🙂",
    "🙃",
    "😉",
    "😌",
    "😍",
    "🥰",
    "😘",
    "😗",
    "😙",
    "😚",
    "😋",
    "😛",
    "😝",
    "😜",
    "🤪",
    "🤨",
    "🧐",
    "🤓",
    "😎",
    "🤩",
    "🥳",
    "😏",
    "😒",
    "😞",
    "😔",
    "😟",
    "😕",
    "🙁",
    "☹️",
    "😣",
    "😖",
    "😫",
    "😩",
    "🥺",
    "😢",
    "😭",
    "😤",
    "😠",
    "😡",
    "🤬",
    "🤯",
    "😳",
    "🥵",
    "🥶",
    "😱",
    "😨",
    "😰",
    "😥",
    "😓",
    "🤗",
    "🤔",
    "🤭",
    "🤫",
    "🤥",
    "😶",
    "😐",
    "😑",
    "😬",
    "🙄",
    "😯",
    "😦",
    "😧",
    "😮",
    "😲",
    "🥱",
    "😴",
    "🤤",
    "😪",
    "😵",
    "🤐",
    "🥴",
    "🤢",
    "🤮",
    "🤧",
    "😷",
    "🤒",
    "🤕",
    "🤑",
    "🤠",
    "😈",
    "👿",
    "👹",
    "👺",
    "🤡",
    "💩",
    "👻",
    "💀",
    "☠️",
    "👽",
    "👾",
    "🤖",
    "🎃",
    "😺",
    "😸",
    "😹",
    "😻",
    "😼",
    "😽",
    "🙀",
    "😿",
    "😾",
    "🙈",
    "🙉",
    "🙊",
    "🐵",
    "🐒",
    "🦊",
    "🐱",
    "🐶",
    "🐻",
    "🐼",
    "🐨",
    "🐯",
    "🦁",
    "🐮",
    "🐷",
    "🐸",
    "🐔",
    "🐧",
    "🐦",
    "🐤",
    "🦄",
    "🐝",
    "🦋",
    "🐢",
    "🐍",
    "🦎",
    "🐙",
    "🦑",
    "🦀",
    "🐠",
    "🐟",
    "🐬",
    "🐳",
    "🦈",
    "🐊",
    "🐘",
    "🦒",
    "🦓",
    "🦌",
    "🐕",
    "🐈",
    "🐓",
    "🦜",
    "🌸",
    "🌹",
    "🌺",
    "🌻",
    "🌼",
    "🌷",
    "🌱",
    "🌿",
    "🍀",
    "🌳",
    "🌴",
    "🌵",
    "🍁",
    "🍂",
    "🍃",
    "🍎",
    "🍊",
    "🍋",
    "🍌",
    "🍉",
    "🍇",
    "🍓",
    "🫐",
    "🍒",
    "🥭",
    "🍍",
    "🥝",
    "🍅",
    "🥑",
    "🍕",
    "🍔",
    "🍟",
    "🌭",
    "🌮",
    "🌯",
    "🍿",
    "🍩",
    "🍪",
    "🎂",
    "🍰",
    "🍫",
    "🍭",
    "☕",
    "🍵",
    "🥤",
    "⚽",
    "🏀",
    "🏈",
    "⚾",
    "🎾",
    "🏐",
    "🏆",
    "🥇",
    "🥈",
    "🥉",
    "🎮",
    "🎯",
    "🎲",
    "🎵",
    "🎶",
    "🎤",
    "🎧",
    "🎸",
    "🎹",
    "🎬",
    "❤️",
    "🧡",
    "💛",
    "💚",
    "💙",
    "💜",
    "🖤",
    "🤍",
    "🤎",
    "💔",
    "❣️",
    "💕",
    "💞",
    "💓",
    "💗",
    "💖",
    "💘",
    "💝",
    "💟",
    "💯",
    "👍",
    "👎",
    "👏",
    "🙌",
    "🫶",
    "🤝",
    "🙏",
    "💪",
    "👋",
    "🤌",
    "✌️",
    "🤞",
    "🤟",
    "🤘",
    "👌",
    "🤏",
    "👈",
    "👉",
    "👆",
    "👇",
    "☝️",
    "✋",
    "🤚",
    "🖐️",
    "🖖",
    "👊",
    "✊",
    "🤲",
    "🤳",
    "💅",
    "🔥",
    "✨",
    "⭐",
    "🌟",
    "💫",
    "💥",
    "💦",
    "💨",
    "🎉",
    "🎊",
    "✅",
    "❌",
    "⚠️",
    "❗",
    "❓",
    "‼️",
    "⁉️",
    "💡",
    "🔔",
    "🔒",
    "🔓",
    "📌",
    "📍",
    "📎",
    "📁",
    "📷",
    "🎥",
    "💻",
    "📱",
    "⌚",
  ];

  const scrollToBottom = () => {
    requestAnimationFrame(() => {
      messagesEndRef.current?.scrollIntoView({
        behavior: "smooth",
      });
    });
  };

  /*
   * =========================================================
   * LOAD CONVERSATIONS
   * Backend route:
   * /api/messaging/conversations/list/
   * =========================================================
   */
  const loadConversations = async () => {
    try {
      setLoadingConversations(true);
      setError("");

      const response = await api.get(
        "/messaging/conversations/list/"
      );

      const data = getListData(response.data);

      setConversations(
        Array.isArray(data)
          ? data
          : []
      );
    } catch (err: any) {
      console.error(
        "Conversation list error:",
        err?.response?.data || err
      );

      setError(
        "Unable to load conversations."
      );
    } finally {
      setLoadingConversations(false);
    }
  };

  /*
   * =========================================================
   * LOAD USERS FOR NEW CHAT
   *
   * We already have current username in localStorage,
   * so there is NO need for /profile/me/.
   *
   * Existing follower routes:
   * /api/followers/{username}/followers/
   * /api/followers/{username}/following/
   * =========================================================
   */
  const loadUsersForNewChat = async () => {
    try {
      setLoadingUsers(true);
      setError("");

      if (!currentUsername) {
        console.error(
          "Current username not found in localStorage."
        );

        setConnections([]);

        setError(
          "Current username was not found. Please login again."
        );

        return;
      }

      const [
        followersResponse,
        followingResponse,
      ] = await Promise.all([
        api.get(
          `/followers/${encodeURIComponent(
            currentUsername
          )}/followers/`
        ),

        api.get(
          `/followers/${encodeURIComponent(
            currentUsername
          )}/following/`
        ),
      ]);

      const followers = getListData(
        followersResponse.data
      );

      const following = getListData(
        followingResponse.data
      );

      const merged =
        new Map<number, ConnectUser>();

      [...followers, ...following].forEach(
        (person: ConnectUser) => {
          if (
            person?.id &&
            Number(person.id) !==
              currentUserId
          ) {
            merged.set(
              Number(person.id),
              {
                ...person,
                id: Number(person.id),
                avatar:
                  person.avatar ||
                  person.profile?.avatar ||
                  null,
              }
            );
          }
        }
      );

      const users = Array.from(
        merged.values()
      ).sort((a, b) =>
        a.username.localeCompare(
          b.username
        )
      );

      setConnections(users);
    } catch (err: any) {
      console.error(
        "Load chat users error:",
        err?.response?.data || err
      );

      setConnections([]);

      setError(
        err?.response?.data?.detail ||
          "Unable to load users."
      );
    } finally {
      setLoadingUsers(false);
    }
  };

  /*
   * =========================================================
   * LOAD MESSAGES
   * Backend route:
   * /api/messaging/conversations/{id}/
   * =========================================================
   */
  const loadMessages = async (
    conversationId: number
  ) => {
    try {
      setLoadingMessages(true);
      setError("");

      const response = await api.get(
        `/messaging/conversations/${conversationId}/`
      );

      const data = getListData(
        response.data
      );

      setMessages(
        Array.isArray(data)
          ? data
          : []
      );

      scrollToBottom();

      /*
       * Mark only this conversation as read.
       */
      await api.patch(
        `/messaging/conversations/${conversationId}/read/`
      );

      setConversations((prev) =>
        prev.map((conversation) =>
          conversation.id ===
          conversationId
            ? {
                ...conversation,
                unread_count: 0,
              }
            : conversation
        )
      );
    } catch (err: any) {
      console.error(
        "Message history error:",
        err?.response?.data || err
      );

      setError(
        err?.response?.data?.detail ||
          "Unable to load messages."
      );

      setMessages([]);
    } finally {
      setLoadingMessages(false);
    }
  };

  const handleSelectConversation =
    async (
      conversation: Conversation
    ) => {
      setSelectedConversationId(
        conversation.id
      );

      const participant =
        conversation.participant;

      if (participant) {
        const realUser =
          userMap.get(
            participant.id
          );

        setSelectedParticipant({
          ...participant,
          ...realUser,
          avatar:
            participant.avatar ||
            participant.profile?.avatar ||
            realUser?.avatar ||
            realUser?.profile?.avatar ||
            null,
        });
      } else {
        setSelectedParticipant(null);
      }

      await loadMessages(
        conversation.id
      );
    };

  /*
   * =========================================================
   * START NEW CONVERSATION
   * Backend route:
   * POST /api/messaging/conversations/
   * =========================================================
   */
  const handleStartConversation =
    async (person: ConnectUser) => {
      try {
        setError("");

        const response =
          await api.post(
            "/messaging/conversations/",
            {
              participant_id:
                person.id,
            }
          );

        const conversationId =
          response.data
            ?.conversation_id;

        if (!conversationId) {
          throw new Error(
            "Conversation ID was not returned."
          );
        }

        const numericConversationId =
          Number(conversationId);

        setShowNewConversation(false);
        setUserSearchText("");

        setSelectedConversationId(
          numericConversationId
        );

        setSelectedParticipant(person);

        await loadConversations();

        /*
         * Load the empty/new conversation.
         */
        await loadMessages(
          numericConversationId
        );

        /*
         * Make sure it appears immediately
         * even if list refresh has not returned it.
         */
        setConversations((prev) => {
          const exists = prev.some(
            (item) =>
              item.id ===
              numericConversationId
          );

          if (exists) {
            return prev;
          }

          const newConversation: Conversation =
            {
              id: numericConversationId,
              participant: person,
              last_message: "",
              last_message_time: null,
              unread_count: 0,
            };

          return [
            newConversation,
            ...prev,
          ];
        });
      } catch (err: any) {
        console.error(
          "Start conversation error:",
          err?.response?.data || err
        );

        setError(
          err?.response?.data
            ?.detail ||
            "Unable to start conversation."
        );
      }
    };

  /*
   * =========================================================
   * SEND MESSAGE
   * Backend route:
   * POST /api/messaging/
   * =========================================================
   */
  const handleSendMessage =
    async () => {
      const text =
        messageText.trim();

      if (
        (!text && !attachment) ||
        !selectedConversationId ||
        sending
      ) {
        return;
      }

      try {
        setSending(true);
        setShowEmojiPicker(false);
        setError("");

        const formData =
          new FormData();

        formData.append(
          "conversation",
          String(
            selectedConversationId
          )
        );

        if (text) {
          formData.append(
            "content",
            text
          );
        }

        if (attachment) {
          formData.append(
            "attachment",
            attachment
          );
        }

        const response =
          await api.post(
            "/messaging/",
            formData,
            
          );

        const sentAttachment =
          attachment;

        setMessageText("");
        setAttachment(null);

        await loadMessages(
          selectedConversationId
        );

        setConversations((prev) =>
          prev.map(
            (conversation) =>
              conversation.id ===
              selectedConversationId
                ? {
                    ...conversation,
                    last_message:
                      response.data
                        ?.content ||
                      (sentAttachment
                        ? "📎 Attachment"
                        : ""),
                    last_message_time:
                      response.data
                        ?.created_at ||
                      new Date().toISOString(),
                  }
                : conversation
          )
        );
      } catch (err: any) {
        console.error(
          "Send message error:",
          err?.response?.data || err
        );

        setError(
          err?.response?.data
            ?.detail ||
            "Unable to send message."
        );
      } finally {
        setSending(false);
      }
    };

  /*
   * =========================================================
   * DELETE MESSAGE
   * Backend route:
   * DELETE /api/messaging/{id}/
   * =========================================================
   */
  const handleDeleteMessage =
    async (
      messageId: number
    ) => {
      try {
        setError("");

        await api.delete(
          `/messaging/${messageId}/`
        );

        if (
          selectedConversationId
        ) {
          await loadMessages(
            selectedConversationId
          );
        }
      } catch (err: any) {
        console.error(
          "Delete message error:",
          err?.response?.data || err
        );

        setError(
          err?.response?.data
            ?.detail ||
            "Unable to delete message."
        );
      }
    };

  const insertEmoji = (
    emoji: string
  ) => {
    setMessageText(
      (previous) =>
        `${previous}${emoji}`
    );
  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  /*
   * =========================================================
   * INITIAL LOAD
   * =========================================================
   */
  useEffect(() => {
    loadConversations();
    loadUsersForNewChat();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  /*
   * =========================================================
   * AUTO REFRESH
   * =========================================================
   */
  useEffect(() => {
    const interval =
      setInterval(() => {
        loadConversations();

        if (
          selectedConversationId
        ) {
          loadMessages(
            selectedConversationId
          );
        }
      }, 8000);

    return () =>
      clearInterval(interval);
  }, [selectedConversationId]);

  /*
   * =========================================================
   * FILTER CONVERSATIONS
   * =========================================================
   */
  const filteredConversations =
    conversations.filter(
      (conversation) => {
        const username =
          conversation
            .participant
            ?.username || "";

        const lastMessage =
          conversation.last_message ||
          "";

        const query =
          searchText
            .trim()
            .toLowerCase();

        if (!query) {
          return true;
        }

        return (
          username
            .toLowerCase()
            .includes(query) ||
          lastMessage
            .toLowerCase()
            .includes(query)
        );
      }
    );

  /*
   * =========================================================
   * FILTER USERS
   * =========================================================
   */
  const filteredUsers =
    connections.filter(
      (person) => {
        const query =
          userSearchText
            .trim()
            .toLowerCase();

        if (!query) {
          return true;
        }

        return (
          person.username
            .toLowerCase()
            .includes(query) ||
          `${person.first_name || ""} ${
            person.last_name || ""
          }`
            .toLowerCase()
            .includes(query)
        );
      }
    );

  const getMessageAvatar = (
    message: Message
  ) => {
    const mappedUser =
      userMap.get(
        message.sender.id
      );

    const avatar =
      message.sender.avatar ||
      mappedUser?.avatar ||
      mappedUser?.profile?.avatar;

    return avatar
      ? getMediaUrl(avatar)
      : defaultProfile;
  };

  return (
    <div className="messagesPage">
      {/* =====================================================
          LEFT SIDEBAR
      ===================================================== */}

      <aside className="sidebar">
        <h2 className="logo">
          ConnectSphere
        </h2>

        <ul>
          <li
  onClick={() => navigate("/home")}
>
  📄 Feed
</li>

<li className="active">
  💬 Messaging
</li>

<li
  onClick={() => navigate("/moderation")}
>
  🛡️ Moderation
</li>
      
          
        </ul>

        <button
          className="createBtn"
          onClick={() =>
            (window.location.href =
              "/create-post")
          }
        >
          Create Post
        </button>

        <button
          className="logoutBtn"
          onClick={() => {
            localStorage.removeItem(
              "access"
            );

            localStorage.removeItem(
              "refresh"
            );

            localStorage.removeItem(
              "user"
            );

            window.location.href =
              "/signin";
          }}
        >
          Logout
        </button>
      </aside>

      {/* =====================================================
          CONVERSATION LIST
      ===================================================== */}

      <section className="messagesListPanel">
        <div className="messagesListHeader">
          <h1>Messages</h1>

          <button
            type="button"
            className="newMessageButton"
            onClick={() => {
              setShowNewConversation(
                true
              );

              setShowEmojiPicker(
                false
              );

              loadUsersForNewChat();
            }}
            title="Start a new conversation"
          >
            ✎
          </button>
        </div>

        <div className="conversationSearchWrapper">
          <span>🔍</span>

          <input
            value={searchText}
            onChange={(event) =>
              setSearchText(
                event.target.value
              )
            }
            placeholder="Search messages..."
          />
        </div>

        {error && (
          <div className="messageError">
            {error}
          </div>
        )}

        <div className="conversationList">
          {loadingConversations ? (
            <div className="emptyMessage">
              Loading conversations...
            </div>
          ) : filteredConversations.length ===
            0 ? (
            <div className="emptyMessage">
              No conversations yet.

              <button
                type="button"
                onClick={() => {
                  setShowNewConversation(
                    true
                  );

                  loadUsersForNewChat();
                }}
              >
                Start a chat
              </button>
            </div>
          ) : (
            filteredConversations.map(
              (conversation) => {
                const participant =
                  conversation.participant;

                const realParticipant =
                  participant
                    ? userMap.get(
                        participant.id
                      )
                    : undefined;

                const avatarUser =
                  participant
                    ? {
                        ...participant,
                        ...realParticipant,
                      }
                    : null;

                return (
                  <button
                    type="button"
                    key={
                      conversation.id
                    }
                    className={`conversationItem ${
                      selectedConversationId ===
                      conversation.id
                        ? "selected"
                        : ""
                    }`}
                    onClick={() =>
                      handleSelectConversation(
                        conversation
                      )
                    }
                  >
                    <img
                      className="conversationAvatar"
                      src={getAvatar(
                        avatarUser
                      )}
                      alt={
                        participant?.username ||
                        "User"
                      }
                    />

                    <div className="conversationInfo">
                      <div className="conversationTopRow">
                        <strong>
                          {participant?.username ||
                            "Unknown User"}
                        </strong>

                        {conversation.last_message_time && (
                          <span>
                            {formatTime(
                              conversation.last_message_time
                            )}
                          </span>
                        )}
                      </div>

                      <div className="conversationBottomRow">
                        <span>
                          {conversation.last_message ||
                            "Start a conversation"}
                        </span>

                        {conversation.unread_count >
                          0 && (
                          <b className="unreadBadge">
                            {conversation.unread_count >
                            99
                              ? "99+"
                              : conversation.unread_count}
                          </b>
                        )}
                      </div>
                    </div>
                  </button>
                );
              }
            )
          )}
        </div>
      </section>

      {/* =====================================================
          CHAT PANEL
      ===================================================== */}

      <main className="chatPanel">
        {!selectedConversationId ? (
          <div className="emptyChatState">
            <div className="emptyChatIcon">
              💬
            </div>

            <h2>
              Select a conversation
            </h2>

            <p>
              Choose someone from your
              conversations or start a new
              chat.
            </p>

            <button
              type="button"
              onClick={() => {
                setShowNewConversation(
                  true
                );

                loadUsersForNewChat();
              }}
            >
              Start New Chat
            </button>
          </div>
        ) : (
          <>
            {/* CHAT HEADER */}

            <header className="chatHeader">
              <div className="chatUserInfo">
                <img
                  className="chatHeaderAvatar"
                  src={getAvatar(
                    selectedParticipant
                  )}
                  alt={
                    selectedParticipant?.username ||
                    "User"
                  }
                />

                <div>
                  <h2>
                    {selectedParticipant?.username ||
                      "User"}
                  </h2>

                  <span>
                    ● Offline
                  </span>
                </div>
              </div>

              <div className="chatHeaderActions">
                <button
                  type="button"
                  title="Video call"
                >
                  📹
                </button>

                <button
                  type="button"
                  title="Voice call"
                >
                  📞
                </button>
              </div>
            </header>

            {/* MESSAGES */}

            <section className="chatMessages">
              {loadingMessages ? (
                <div className="emptyChatState">
                  Loading messages...
                </div>
              ) : messages.length ===
                0 ? (
                <div className="emptyChatState">
                  <div className="emptyChatIcon">
                    👋
                  </div>

                  <h3>
                    No messages yet
                  </h3>

                  <p>
                    Send the first message.
                  </p>
                </div>
              ) : (
                messages.map(
                  (message) => {
                    const isMine =
                      Number(
                        message.sender?.id
                      ) ===
                      currentUserId;

                    return (
                      <div
                        key={
                          message.id
                        }
                        className={`messageRow ${
                          isMine
                            ? "mine"
                            : "theirs"
                        }`}
                      >
                        {!isMine && (
                          <img
                            className="messageAvatar"
                            src={getMessageAvatar(
                              message
                            )}
                            alt={
                              message
                                .sender
                                ?.username ||
                              "User"
                            }
                          />
                        )}

                        <div
                          className={`messageBubble ${
                            isMine
                              ? "mine"
                              : "theirs"
                          }`}
                        >
                          <div className="messageContent">
                            {
                              message.content
                            }
                          </div>

                          {message.attachment && (
                            <a
                              href={getMediaUrl(
                                message.attachment
                              )}
                              target="_blank"
                              rel="noreferrer"
                              className="messageAttachment"
                            >
                              📎 Open attachment
                            </a>
                          )}

                          <div className="messageMeta">
                            <span>
                              {formatTime(
                                message.created_at
                              )}
                            </span>

                            {isMine && (
                              <span
                                title={
                                  message.is_read
                                    ? "Seen"
                                    : "Sent"
                                }
                              >
                                {message.is_read
                                  ? "✓✓"
                                  : "✓"}
                              </span>
                            )}

                            {isMine && (
                              <button
                                type="button"
                                className="deleteMessageButton"
                                onClick={() =>
                                  handleDeleteMessage(
                                    message.id
                                  )
                                }
                                title="Delete message"
                              >
                                🗑️
                              </button>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  }
                )
              )}

              <div
                ref={
                  messagesEndRef
                }
              />
            </section>

            {/* COMPOSER */}

            <footer className="messageComposer">
              {attachment && (
                <div className="attachmentPreview">
                  <span>
                    📎{" "}
                    {attachment.name}
                  </span>

                  <button
                    type="button"
                    onClick={() =>
                      setAttachment(
                        null
                      )
                    }
                  >
                    ✕
                  </button>
                </div>
              )}

              <div className="composerRow">
                <button
                  type="button"
                  className="composerIconButton"
                  onClick={() =>
                    fileInputRef.current?.click()
                  }
                  title="Attach file"
                >
                  📎
                </button>

                <input
                  ref={fileInputRef}
                  type="file"
                  hidden
                  onChange={(event) => {
                    const file =
                      event.target.files?.[0];

                    if (file) {
                      setAttachment(
                        file
                      );
                    }

                    event.currentTarget.value =
                      "";
                  }}
                />

                <div className="emojiWrapper">
                  <button
                    type="button"
                    className="composerIconButton"
                    onClick={() =>
                      setShowEmojiPicker(
                        (previous) =>
                          !previous
                      )
                    }
                    title="Emoji"
                  >
                    😊
                  </button>

                  {showEmojiPicker && (
                    <div className="emojiPicker">
                      <div className="emojiPickerHeader">
                        <strong>
                          Emojis
                        </strong>

                        <button
                          type="button"
                          onClick={() =>
                            setShowEmojiPicker(
                              false
                            )
                          }
                        >
                          ✕
                        </button>
                      </div>

                      <div className="emojiGrid">
                        {emojis.map(
                          (
                            emoji,
                            index
                          ) => (
                            <button
                              type="button"
                              key={`${emoji}-${index}`}
                              onClick={() =>
                                insertEmoji(
                                  emoji
                                )
                              }
                            >
                              {emoji}
                            </button>
                          )
                        )}
                      </div>
                    </div>
                  )}
                </div>

                <input
                  className="messageInput"
                  value={messageText}
                  onChange={(event) =>
                    setMessageText(
                      event.target.value
                    )
                  }
                  onKeyDown={
                    handleKeyDown
                  }
                  placeholder={`Message ${
                    selectedParticipant?.username ||
                    "User"
                  }...`}
                />

                <button
                  type="button"
                  className="sendMessageButton"
                  onClick={
                    handleSendMessage
                  }
                  disabled={
                    sending ||
                    (!messageText.trim() &&
                      !attachment)
                  }
                  title="Send message"
                >
                  ➤
                </button>
              </div>
            </footer>
          </>
        )}
      </main>

      {/* =====================================================
          NEW CONVERSATION MODAL
      ===================================================== */}

      {showNewConversation && (
        <div
          className="newConversationOverlay"
          onClick={() =>
            setShowNewConversation(
              false
            )
          }
        >
          <div
            className="newConversationModal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >
            <div className="newConversationHeader">
              <div>
                <h2>
                  New Conversation
                </h2>

                <p>
                  Select a username to
                  start chatting.
                </p>
              </div>

              <button
                type="button"
                onClick={() =>
                  setShowNewConversation(
                    false
                  )
                }
              >
                ✕
              </button>
            </div>

            <div className="userSearch">
              <span>🔍</span>

              <input
                value={userSearchText}
                onChange={(event) =>
                  setUserSearchText(
                    event.target.value
                  )
                }
                placeholder="Search username..."
                autoFocus
              />
            </div>

            <div className="newConversationUsers">
              {loadingUsers ? (
                <div className="emptyMessage">
                  Loading users...
                </div>
              ) : filteredUsers.length ===
                0 ? (
                <div className="emptyMessage">
                  No users found.
                </div>
              ) : (
                filteredUsers.map(
                  (person) => (
                    <button
                      type="button"
                      className="selectUserItem"
                      key={
                        person.id
                      }
                      onClick={() =>
                        handleStartConversation(
                          person
                        )
                      }
                    >
                      <img
                        src={getAvatar(
                          person
                        )}
                        alt={
                          person.username
                        }
                      />

                      <div>
                        <strong>
                          {
                            person.username
                          }
                        </strong>

                        {(person.first_name ||
                          person.last_name) && (
                          <span>
                            {[
                              person.first_name,
                              person.last_name,
                            ]
                              .filter(
                                Boolean
                              )
                              .join(
                                " "
                              )}
                          </span>
                        )}
                      </div>

                      <span className="selectArrow">
                        →
                      </span>
                    </button>
                  )
                )
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
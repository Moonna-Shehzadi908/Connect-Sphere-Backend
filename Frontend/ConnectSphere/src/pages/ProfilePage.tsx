import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import "./ProfilePage.css";

import {
  getMyProfile,
  updateProfile,
  uploadAvatar,
  uploadCover,
} from "../services/profile";

import api from "../services/api";

import defaultProfile from "../assets/profile icone.webp";

// ==========================================================
// TYPES
// ==========================================================

interface Profile {
  id: number;
  username: string;
  email: string;

  profile: {
    bio: string;
    website: string;
    location: string;
    birth_date: string;

    avatar: string | null;
    cover_photo: string | null;
  };
}

interface FollowUser {
  id: number;
  username: string;
  first_name?: string;
  last_name?: string;
  avatar: string | null;
}

interface ProfileStats {
  followers: number;
  following: number;
}

// ==========================================================
// COMPONENT
// ==========================================================

export default function ProfilePage() {
  const navigate = useNavigate();

  // ========================================================
  // PROFILE STATES
  // ========================================================

  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const avatarInputRef = useRef<HTMLInputElement>(null);
  const coverInputRef = useRef<HTMLInputElement>(null);

  // ========================================================
  // PROFILE FORM
  // ========================================================

  const [formData, setFormData] = useState({
    bio: "",
    website: "",
    location: "",
    birth_date: "",
  });

  // ========================================================
  // FOLLOWER STATES
  // ========================================================

  const [stats, setStats] = useState<ProfileStats>({
    followers: 0,
    following: 0,
  });

  const [followers, setFollowers] = useState<FollowUser[]>([]);
  const [following, setFollowing] = useState<FollowUser[]>([]);
  const [suggestions, setSuggestions] = useState<FollowUser[]>([]);

  const [followLoading, setFollowLoading] = useState<number | null>(null);

  const [activeFollowTab, setActiveFollowTab] = useState<
    "followers" | "following" | null
  >(null);

  const [loadingFollowData, setLoadingFollowData] = useState(false);

  // ========================================================
  // MEDIA URL
  // ========================================================

  const getMediaUrl = (path: string | null | undefined) => {
    if (!path) return "";

    if (
      path.startsWith("http://") ||
      path.startsWith("https://")
    ) {
      return path;
    }

    return `http://127.0.0.1:8000${
      path.startsWith("/") ? path : `/${path}`
    }`;
  };

  // ========================================================
  // LOAD PROFILE
  // ========================================================

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
  try {
    setLoading(true);

    const data = await getMyProfile();

    console.log("PROFILE RESPONSE:", data);
    console.log("USER:", data?.user);
    console.log("USERNAME:", data?.user?.username);

    // =====================================================
    // BACKEND RESPONSE:
    //
    // {
    //   user: {
    //     id,
    //     username,
    //     email
    //   },
    //   profile: {
    //     bio,
    //     website,
    //     location,
    //     birth_date,
    //     avatar,
    //     cover_photo
    //   }
    // }
    //
    // Normalize it so the rest of ProfilePage can keep using:
    // profile.username
    // profile.email
    // profile.profile
    // =====================================================

    const normalizedProfile: Profile = {
      id: data?.user?.id,
      username: data?.user?.username,
      email: data?.user?.email,

      profile: {
        bio: data?.profile?.bio || "",
        website: data?.profile?.website || "",
        location: data?.profile?.location || "",
        birth_date: data?.profile?.birth_date || "",
        avatar: data?.profile?.avatar || null,
        cover_photo: data?.profile?.cover_photo || null,
      },
    };

    console.log(
      "NORMALIZED PROFILE:",
      normalizedProfile
    );

    console.log(
      "CALLING FOLLOW DATA FOR:",
      normalizedProfile.username
    );

    setProfile(normalizedProfile);

    setFormData({
      bio: normalizedProfile.profile.bio,
      website: normalizedProfile.profile.website,
      location: normalizedProfile.profile.location,
      birth_date: normalizedProfile.profile.birth_date,
    });

    // =====================================================
    // LOAD FOLLOWERS / FOLLOWING
    // =====================================================

    if (normalizedProfile.username) {
      await loadFollowData(
        normalizedProfile.username
      );
    } else {
      console.error(
        "❌ USERNAME NOT FOUND — FOLLOW API NOT CALLED"
      );
    }

  } catch (err) {
    console.error(
      "Load profile error:",
      err
    );
  } finally {
    setLoading(false);
  }
};
  // ========================================================
  // LOAD FOLLOWERS / FOLLOWING / STATS / SUGGESTIONS
  // ========================================================

  const loadFollowData = async (username: string) => {
    try {
      setLoadingFollowData(true);

      const [
        statsResponse,
        followersResponse,
        followingResponse,
        suggestionsResponse,
      ] = await Promise.all([
        // GET /api/followers/<username>/stats/
        api.get(`/followers/${username}/stats/`),

        // GET /api/followers/<username>/followers/
        api.get(`/followers/${username}/followers/`),

        // GET /api/followers/<username>/following/
        api.get(`/followers/${username}/following/`),

        // GET /api/followers/friend-suggestions/
        api.get(`/followers/friend-suggestions/`),
      ]);

      // ====================================================
      // STATS
      // ====================================================

      setStats({
        followers: Number(
          statsResponse.data?.followers ?? 0
        ),

        following: Number(
          statsResponse.data?.following ?? 0
        ),
      });

      // ====================================================
      // FOLLOWERS
      // ====================================================

      setFollowers(
        Array.isArray(followersResponse.data)
          ? followersResponse.data
          : []
      );

      // ====================================================
      // FOLLOWING
      // ====================================================

      setFollowing(
        Array.isArray(followingResponse.data)
          ? followingResponse.data
          : []
      );

      // ====================================================
      // FRIEND SUGGESTIONS
      // ====================================================

      setSuggestions(
        Array.isArray(suggestionsResponse.data)
          ? suggestionsResponse.data
          : []
      );
    } catch (error: any) {
      console.error(
        "Load followers data error:",
        error?.response?.data || error
      );

      // Don't destroy previous working UI
      setStats({
        followers: 0,
        following: 0,
      });

      setFollowers([]);
      setFollowing([]);
      setSuggestions([]);
    } finally {
      setLoadingFollowData(false);
    }
  };

  // ========================================================
  // HANDLE FORM INPUT
  // ========================================================

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement
    >
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // ========================================================
  // SAVE PROFILE
  // ========================================================

  const handleSave = async () => {
    try {
      setSaving(true);

      const fd = new FormData();

      fd.append("bio", formData.bio);
      fd.append("website", formData.website);
      fd.append("location", formData.location);
      fd.append("birth_date", formData.birth_date);

      await updateProfile(fd);

      await loadProfile();

      alert("Profile updated successfully.");
    } catch (err: any) {
      console.log(
        "Update profile error:",
        err?.response
      );

      if (err?.response?.data) {
        alert(
          JSON.stringify(err.response.data)
        );
      } else {
        alert(
          err?.message ||
            "Failed to update profile."
        );
      }
    } finally {
      setSaving(false);
    }
  };

  // ========================================================
  // UPLOAD AVATAR
  // ========================================================

  const handleAvatar = async (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    if (!e.target.files?.length) {
      return;
    }

    try {
      const fd = new FormData();

      fd.append(
        "avatar",
        e.target.files[0]
      );

      await uploadAvatar(fd);

      await loadProfile();

      alert(
        "Profile picture updated successfully."
      );
    } catch (err) {
      console.error(
        "Avatar upload error:",
        err
      );

      alert(
        "Failed to upload profile picture."
      );
    }
  };

  // ========================================================
  // UPLOAD COVER
  // ========================================================

  const handleCover = async (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    if (!e.target.files?.length) {
      return;
    }

    try {
      const fd = new FormData();

      fd.append(
        "cover_photo",
        e.target.files[0]
      );

      await uploadCover(fd);

      await loadProfile();

      alert(
        "Cover photo updated successfully."
      );
    } catch (err) {
      console.error(
        "Cover upload error:",
        err
      );

      alert(
        "Failed to upload cover photo."
      );
    }
  };

  // ========================================================
  // FOLLOW USER
  // ========================================================

  const handleFollow = async (
    username: string,
    userId: number
  ) => {
    try {
      setFollowLoading(userId);

      // POST /api/followers/follow/<username>/
      const response = await api.post(
        `/followers/follow/${username}/`
      );

      console.log(
        "Follow response:",
        response.data
      );

      // Remove user from suggestions immediately
      setSuggestions((prev) =>
        prev.filter(
          (user) => user.id !== userId
        )
      );

      // Refresh all follower information
      if (profile?.username) {
        await loadFollowData(
          profile.username
        );
      }

      alert(
        `You are now following ${username}.`
      );
    } catch (error: any) {
      console.error(
        "Follow error:",
        error?.response?.data || error
      );

      const message =
        error?.response?.data?.message ||
        "Failed to follow user.";

      alert(message);
    } finally {
      setFollowLoading(null);
    }
  };

  // ========================================================
  // UNFOLLOW USER
  // ========================================================

  const handleUnfollow = async (
    username: string,
    userId: number
  ) => {
    try {
      setFollowLoading(userId);

      // DELETE /api/followers/unfollow/<username>/
      const response = await api.delete(
        `/followers/unfollow/${username}/`
      );

      console.log(
        "Unfollow response:",
        response.data
      );

      // Refresh follower information
      if (profile?.username) {
        await loadFollowData(
          profile.username
        );
      }

      alert(
        `You have unfollowed ${username}.`
      );
    } catch (error: any) {
      console.error(
        "Unfollow error:",
        error?.response?.data || error
      );

      const message =
        error?.response?.data?.message ||
        "Failed to unfollow user.";

      alert(message);
    } finally {
      setFollowLoading(null);
    }
  };

  // ========================================================
  // CHECK IF CURRENT USER IS FOLLOWING SOMEONE
  // ========================================================

  const isFollowing = (
    userId: number
  ) => {
    return following.some(
      (user) => user.id === userId
    );
  };

  // ========================================================
  // FOLLOWER / FOLLOWING TAB
  // ========================================================

  const handleFollowTab = (
    tab: "followers" | "following"
  ) => {
    setActiveFollowTab(
      (previous) =>
        previous === tab ? null : tab
    );
  };

  // ========================================================
  // LOADING
  // ========================================================

  if (loading) {
    return (
      <div className="profilePage">
        <h2>
          Loading Profile...
        </h2>
      </div>
    );
  }

  // ========================================================
  // RENDER
  // ========================================================

  return (
    <div className="profilePage">

      {/* ==================================================
          BACK BUTTON
      ================================================== */}

      <button
        className="backBtn"
        onClick={() =>
          navigate("/home")
        }
      >
        ← Back to Feed
      </button>

      {/* ==================================================
          COVER
      ================================================== */}

      <div className="coverSection">

        <img
          className="coverImage"
          src={
            profile?.profile?.cover_photo
              ? getMediaUrl(
                  profile.profile.cover_photo
                )
              : "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1600"
          }
          alt="Cover"
        />

        <button
          className="coverEditBtn"
          onClick={() =>
            coverInputRef.current?.click()
          }
        >
          📷 Edit Cover
        </button>

        <input
          type="file"
          accept="image/*"
          ref={coverInputRef}
          hidden
          onChange={handleCover}
        />

      </div>

      {/* ==================================================
          PROFILE HEADER
      ================================================== */}

      <div className="profileHeader">

        <div className="avatarWrapper">

          <img
            className="avatar"
            src={
              profile?.profile?.avatar
                ? getMediaUrl(
                    profile.profile.avatar
                  )
                : defaultProfile
            }
            alt="Profile"
          />

          <button
            className="avatarEditBtn"
            onClick={() =>
              avatarInputRef.current?.click()
            }
          >
            📷
          </button>

          <input
            type="file"
            accept="image/*"
            ref={avatarInputRef}
            hidden
            onChange={handleAvatar}
          />

        </div>

        <h2 className="header-heading">
          {profile?.username}
        </h2>

        <p>
          {profile?.email}
        </p>

        {/* ==================================================
            FOLLOWER STATS
        ================================================== */}

        <div className="followStats">

          <button
            type="button"
            className="followStatBtn"
            onClick={() =>
              handleFollowTab(
                "followers"
              )
            }
          >
            <strong>
              {stats.followers}
            </strong>

            <span>
              Followers
            </span>
          </button>

          <button
            type="button"
            className="followStatBtn"
            onClick={() =>
              handleFollowTab(
                "following"
              )
            }
          >
            <strong>
              {stats.following}
            </strong>

            <span>
              Following
            </span>
          </button>

        </div>

      </div>

      {/* ==================================================
          FOLLOWERS / FOLLOWING LIST
      ================================================== */}

      {activeFollowTab && (
        <div className="followListCard">

          <div className="followListHeader">

            <h3>
              {activeFollowTab ===
              "followers"
                ? "Followers"
                : "Following"}
            </h3>

            <button
              type="button"
              className="followListClose"
              onClick={() =>
                setActiveFollowTab(
                  null
                )
              }
            >
              ✕
            </button>

          </div>

          {loadingFollowData ? (
            <p className="followLoadingText">
              Loading...
            </p>
          ) : (
            <div className="followUsersList">

              {(
                activeFollowTab ===
                "followers"
                  ? followers
                  : following
              ).length === 0 ? (
                <p className="noFollowUsers">
                  No{" "}
                  {activeFollowTab ===
                  "followers"
                    ? "followers"
                    : "following"}{" "}
                  yet.
                </p>
              ) : (
                (
                  activeFollowTab ===
                  "followers"
                    ? followers
                    : following
                ).map((person) => (

                  <div
                    className="followUserItem"
                    key={person.id}
                  >

                    <img
                      src={
                        person.avatar
                          ? getMediaUrl(
                              person.avatar
                            )
                          : defaultProfile
                      }
                      alt={
                        person.username
                      }
                    />

                    <div className="followUserInfo">

                      <strong>
                        {person.username}
                      </strong>

                      {(person.first_name ||
                        person.last_name) && (
                        <span>
                          {[
                            person.first_name,
                            person.last_name,
                          ]
                            .filter(Boolean)
                            .join(" ")}
                        </span>
                      )}

                    </div>

                    {/* Follow/Unfollow
                        in Followers tab */}

                    {activeFollowTab ===
                      "followers" &&
                      person.id !==
                        profile?.id && (

                        <button
                          type="button"
                          className={
                            isFollowing(
                              person.id
                            )
                              ? "followingBtn"
                              : "followBtn"
                          }
                          disabled={
                            followLoading ===
                            person.id
                          }
                          onClick={() =>
                            isFollowing(
                              person.id
                            )
                              ? handleUnfollow(
                                  person.username,
                                  person.id
                                )
                              : handleFollow(
                                  person.username,
                                  person.id
                                )
                          }
                        >
                          {followLoading ===
                          person.id
                            ? "..."
                            : isFollowing(
                                person.id
                              )
                            ? "Following"
                            : "Follow"}
                        </button>
                    )}

                  </div>
                ))
              )}

            </div>
          )}

        </div>
      )}

      {/* ==================================================
          FRIEND SUGGESTIONS
      ================================================== */}

      <div className="suggestionsCard">

        <div className="suggestionsHeader">

          <h3>
            👥 People You May Know
          </h3>

          <button
            type="button"
            className="refreshSuggestionsBtn"
            onClick={() => {
              if (profile?.username) {
                loadFollowData(
                  profile.username
                );
              }
            }}
          >
            🔄
          </button>

        </div>

        {loadingFollowData ? (
          <p className="followLoadingText">
            Loading suggestions...
          </p>
        ) : suggestions.length === 0 ? (
          <p className="noFollowUsers">
            No new people to suggest.
          </p>
        ) : (
          <div className="suggestionsList">

            {suggestions.map(
              (person) => (

                <div
                  className="suggestionItem"
                  key={person.id}
                >

                  <img
                    src={
                      person.avatar
                        ? getMediaUrl(
                            person.avatar
                          )
                        : defaultProfile
                    }
                    alt={
                      person.username
                    }
                  />

                  <div className="suggestionInfo">

                    <strong>
                      {person.username}
                    </strong>

                    {(person.first_name ||
                      person.last_name) && (
                      <span>
                        {[
                          person.first_name,
                          person.last_name,
                        ]
                          .filter(Boolean)
                          .join(" ")}
                      </span>
                    )}

                  </div>

                  <button
                    type="button"
                    className="followBtn"
                    disabled={
                      followLoading ===
                      person.id
                    }
                    onClick={() =>
                      handleFollow(
                        person.username,
                        person.id
                      )
                    }
                  >
                    {followLoading ===
                    person.id
                      ? "..."
                      : "Follow"}
                  </button>

                </div>
              )
            )}

          </div>
        )}

      </div>

      {/* ==================================================
          PROFILE FORM
      ================================================== */}

      <div className="profileCard">

        <h3>
          Edit Profile
        </h3>

        <label>
          Bio
        </label>

        <textarea
          name="bio"
          rows={4}
          value={formData.bio}
          onChange={handleChange}
          placeholder="Tell everyone about yourself..."
        />

        <label>
          Website
        </label>

        <input
          type="text"
          name="website"
          value={formData.website}
          onChange={handleChange}
          placeholder="https://yourwebsite.com"
        />

        <label>
          Location
        </label>

        <input
          type="text"
          name="location"
          value={formData.location}
          onChange={handleChange}
          placeholder="Pakistan"
        />

        <label>
          Birth Date
        </label>

        <input
          type="date"
          name="birth_date"
          value={formData.birth_date}
          onChange={handleChange}
        />

        <button
          type="button"
          className="saveBtn"
          onClick={handleSave}
          disabled={saving}
        >
          {saving
            ? "Saving..."
            : "💾 Save Changes"}
        </button>

      </div>

    </div>
  );
}
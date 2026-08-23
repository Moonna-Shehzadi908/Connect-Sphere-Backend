import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./CreatePostPage.css";
import profile from "../assets/profile icone.jpg";
import { createPost } from "../services/postApi";

export default function CreatePostPage() {
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("Technology");
  const [audience, setAudience] = useState("Public");
  const [hashtags, setHashtags] = useState("");
  const [image, setImage] = useState<File | null>(null);

  const [publishing, setPublishing] = useState(false);

  // ==========================
  // LOGOUT
  // ==========================

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");

    alert("Logged out successfully!");

    navigate("/signin", { replace: true });
  };

  // ==========================
  // PUBLISH POST
  // ==========================

  const handlePublish = async () => {
    if (!title.trim() || !description.trim()) {
      alert("Please enter title and description.");
      return;
    }

    try {
      setPublishing(true);

      /*
       * Backend currently supports:
       * - content
       * - visibility
       * - images
       *
       * Title and category are not separate backend fields.
       * Therefore title + description + hashtags are combined
       * into the content field.
       */

      let content = `${title.trim()}\n\n${description.trim()}`;

      if (hashtags.trim()) {
        content += `\n\n${hashtags.trim()}`;
      }

      /*
       * Backend supports:
       * PUBLIC
       * PRIVATE
       *
       * Followers is not currently supported by backend.
       * So Followers currently behaves as PUBLIC.
       */

      const visibility =
        audience === "Private"
          ? "PRIVATE"
          : "PUBLIC";

      /*
       * Send content, visibility and image separately.
       * createPost() will create the FormData and send
       * the request to POST /posts/.
       */

     await createPost(
  content,
  visibility,
  image
);

      alert("✅ Post published successfully.");

      // Clear form
      setTitle("");
      setDescription("");
      setCategory("Technology");
      setAudience("Public");
      setHashtags("");
      setImage(null);

      // Return to HomeFeed
      navigate("/home");

    } catch (error: any) {
      console.error(
        "Create post error:",
        error
      );

      if (error.response?.data) {
        console.error(
          "Backend response:",
          error.response.data
        );

        alert(
          typeof error.response.data === "string"
            ? error.response.data
            : JSON.stringify(
                error.response.data
              )
        );
      } else {
        alert(
          "❌ Failed to publish post. Please try again."
        );
      }

    } finally {
      setPublishing(false);
    }
  };

  // ==========================
  // SAVE DRAFT
  // ==========================

  const handleDraft = () => {
    alert(
      "📂 Draft feature is not connected to the backend yet."
    );
  };

  // ==========================
  // PREVIEW
  // ==========================

  const handlePreview = () => {
    alert("👀 Live Preview Updated.");
  };

  // ==========================
  // CLEAR FORM
  // ==========================

  const handleClear = () => {
    setTitle("");
    setDescription("");
    setCategory("Technology");
    setAudience("Public");
    setHashtags("");
    setImage(null);

    alert("Form cleared.");
  };

  // ==========================
  // IMAGE SELECT
  // ==========================

  const handleImageChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    if (e.target.files?.length) {
      setImage(e.target.files[0]);
    }
  };

  // ==========================
  // IMAGE PREVIEW
  // ==========================

  const imagePreview = image
    ? URL.createObjectURL(image)
    : null;

  return (
    <div className="createPostPage">

      {/* ==========================
          SIDEBAR
      ========================== */}

      <aside className="sidebar">

        <h2 className="logo">
          ConnectSphere
        </h2>

        <ul>

          <li
            onClick={() =>
              navigate("/home")
            }
          >
            📄 Feed
          </li>

          <li
            onClick={() =>
              navigate("/messages")
            }
          >
            💬 Messaging
          </li>

         

        

          <li
            onClick={() =>
              navigate("/moderation")
            }
          >
            🛡 Moderation
          </li>

         

        </ul>

        <button className="createBtn">
          Create Post
        </button>

        <button
          className="logoutBtn"
          onClick={handleLogout}
        >
          Logout
        </button>

        <button
          className="backBtn"
          onClick={() =>
            navigate("/home")
          }
        >
          ← Back
        </button>

      </aside>

      {/* ==========================
          MAIN CONTENT
      ========================== */}

      <main className="mainContent">

        <h1 className="pageTitle">
          Create New Post
        </h1>

        <p className="pageSubTitle">
          Share ideas, updates and professional
          insights with your ConnectSphere community.
        </p>

        <div className="formCard">

          {/* ==========================
              TITLE
          ========================== */}

          <div className="formGroup">

            <label>
              Post Title *
            </label>

            <input
              type="text"
              placeholder="Example: The Future of Artificial Intelligence"
              value={title}
              onChange={(e) =>
                setTitle(e.target.value)
              }
            />

          </div>

          {/* ==========================
              DESCRIPTION
          ========================== */}

          <div className="formGroup">

            <label>
              Description *
            </label>

            <textarea
              placeholder="Write a professional post that engages your audience..."
              value={description}
              onChange={(e) =>
                setDescription(e.target.value)
              }
            />

          </div>

          {/* ==========================
              CATEGORY & AUDIENCE
          ========================== */}

          <div className="row">

            <div className="formGroup">

              <label>
                Category
              </label>

              <select
                value={category}
                onChange={(e) =>
                  setCategory(e.target.value)
                }
              >

                <option value="Technology">
                  Technology
                </option>

                <option value="Business">
                  Business
                </option>

                <option value="Design">
                  Design
                </option>

                <option value="Marketing">
                  Marketing
                </option>

                <option value="Education">
                  Education
                </option>

                <option value="Career">
                  Career
                </option>

              </select>

            </div>

            <div className="formGroup">

              <label>
                Audience
              </label>

              <select
                value={audience}
                onChange={(e) =>
                  setAudience(e.target.value)
                }
              >

                <option value="Public">
                  Public
                </option>

                <option value="Private">
                  Private
                </option>

                <option value="Followers">
                  Followers
                </option>

              </select>

              <small className="helperText">
                Followers visibility is not supported
                by the current backend yet.
              </small>

            </div>

          </div>

          {/* ==========================
              HASHTAGS
          ========================== */}

          <div className="formGroup">

            <label>
              Hashtags
            </label>

            <input
              className="hashInput"
              type="text"
              placeholder="#technology #react #career"
              value={hashtags}
              onChange={(e) =>
                setHashtags(e.target.value)
              }
            />

            <small className="helperText">
              Add relevant hashtags to increase
              your post reach.
            </small>

          </div>

          {/* ==========================
              IMAGE UPLOAD
          ========================== */}

          <div className="formGroup">

            <label>
              Upload Image
            </label>

            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
            />

            <small className="helperText">
              JPG, PNG or WEBP • Max size 5 MB
            </small>

            {imagePreview && (
              <div className="previewImage">

                <img
                  src={imagePreview}
                  alt="Selected preview"
                />

              </div>
            )}

          </div>

          {/* ==========================
              BUTTONS
          ========================== */}

          <div className="buttonGroup">

            <button
              className="draftBtn"
              onClick={handleDraft}
              disabled={publishing}
            >
              💾 Save Draft
            </button>

            <button
              className="previewBtn"
              onClick={handlePreview}
              disabled={publishing}
            >
              👀 Preview
            </button>

            <button
              className="publishBtn"
              onClick={handlePublish}
              disabled={publishing}
            >
              {publishing
                ? "⏳ Publishing..."
                : "🚀 Publish Post"}
            </button>

            <button
              className="clearBtn"
              onClick={handleClear}
              disabled={publishing}
            >
              🗑 Clear Form
            </button>

          </div>

        </div>

      </main>

      {/* ==========================
          LIVE PREVIEW PANEL
      ========================== */}

      <aside className="previewPanel">

        <h2>
          Live Preview
        </h2>

        <div className="previewCard">

          <div className="previewHeader">

            <img
              src={profile}
              alt="Profile"
            />

            <div>

              <h3>
                Your Profile
              </h3>

              <span>
                {audience}
              </span>

            </div>

          </div>

          <div className="previewCategory">
            {category}
          </div>

          <h2>
            {title || "Your post title"}
          </h2>

          <p>
            {description ||
              "Your post description will appear here as users will see it after publishing."}
          </p>

          {hashtags && (
            <div className="hashtags">
              {hashtags}
            </div>
          )}

          {imagePreview && (
            <img
              className="postPreviewImage"
              src={imagePreview}
              alt="Post preview"
            />
          )}

          <div className="previewFooter">

            <span>
              ❤️ 0 Likes
            </span>

            <span>
              💬 0 Comments
            </span>

            <span>
              ↗ Share
            </span>

          </div>

        </div>

      </aside>

    </div>
  );
}
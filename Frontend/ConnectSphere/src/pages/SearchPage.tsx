import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import "./SearchPage.css";

interface UserResult {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
}

interface PostAuthor {
  id: number;
  username: string;
}

interface PostResult {
  id: number;
  author: PostAuthor;
  content: string;
  created_at: string;
}

interface HashtagResult {
  id: number;
  name: string;
  posts_count: number;
}

interface SearchResults {
  users: UserResult[];
  posts: PostResult[];
  hashtags: HashtagResult[];
}

export default function SearchPage() {
  const navigate = useNavigate();

  const [searchQuery, setSearchQuery] = useState("");

  const [results, setResults] = useState<SearchResults>({
    users: [],
    posts: [],
    hashtags: [],
  });

  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");

  // ==========================================================
  // SEARCH
  // ==========================================================

  const handleSearch = async () => {
    const query = searchQuery.trim();

    if (!query) {
      setResults({
        users: [],
        posts: [],
        hashtags: [],
      });

      setSearched(false);
      setError("");

      return;
    }

    try {
      setLoading(true);
      setSearched(true);
      setError("");

      /*
       * Backend endpoint:
       *
       * GET /api/search/?q=moona
       *
       * Existing api service is used so that the
       * authentication token is automatically attached.
       */

      const response = await api.get("/search/", {
        params: {
          q: query,
        },
      });

      const data: SearchResults = response.data;

      setResults({
        users: data.users || [],
        posts: data.posts || [],
        hashtags: data.hashtags || [],
      });
    } catch (error: any) {
      console.error("Search error:", error);

      setError(
        "Unable to perform search. Please check your connection and try again."
      );

      setResults({
        users: [],
        posts: [],
        hashtags: [],
      });
    } finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // CLEAR SEARCH
  // ==========================================================

  const clearSearch = () => {
    setSearchQuery("");

    setResults({
      users: [],
      posts: [],
      hashtags: [],
    });

    setSearched(false);
    setError("");
  };

  // ==========================================================
  // RENDER
  // ==========================================================

  return (
    <div className="searchPage">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="searchHeader">

        <button
          className="backButton"
          onClick={() => navigate("/home")}
        >
          ←
        </button>

        <div className="searchLogo">
          ConnectSphere
        </div>

        <h1>Search</h1>

      </header>

      {/* =====================================================
          MAIN
      ===================================================== */}

      <main className="searchContainer">

        {/* ===================================================
            SEARCH BOX
        =================================================== */}

        <div className="searchBox">

          <span className="searchIcon">
            🔍
          </span>

          <input
            type="text"
            placeholder="Search people, posts, hashtags..."
            value={searchQuery}
            onChange={(e) =>
              setSearchQuery(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSearch();
              }
            }}
          />

          {searchQuery && (
            <button
              className="clearSearch"
              onClick={clearSearch}
              aria-label="Clear search"
            >
              ✕
            </button>
          )}

          <button
            className="searchButton"
            onClick={handleSearch}
            disabled={loading}
          >
            {loading ? "Searching..." : "Search"}
          </button>

        </div>

        {/* ===================================================
            ERROR
        =================================================== */}

        {error && (
          <div className="searchError">
            {error}
          </div>
        )}

        {/* ===================================================
            RESULTS
        =================================================== */}

        <section className="searchResults">

          {/* =================================================
              INITIAL STATE
          ================================================= */}

          {!searched && !loading && (
            <div className="emptySearch">

              <div className="emptySearchIcon">
                🔍
              </div>

              <h2>
                Discover on ConnectSphere
              </h2>

              <p>
                Search for people, posts and hashtags.
              </p>

            </div>
          )}

          {/* =================================================
              LOADING
          ================================================= */}

          {loading && (
            <div className="emptySearch">

              <div className="emptySearchIcon">
                🔄
              </div>

              <h2>
                Searching...
              </h2>

              <p>
                Finding results for "{searchQuery}"
              </p>

            </div>
          )}

          {/* =================================================
              SEARCH RESULTS
          ================================================= */}

          {searched &&
            !loading &&
            !error && (

              <div className="resultsContainer">

                <h2 className="resultsTitle">
                  Search Results
                </h2>

                <p className="resultsFor">
                  Results for{" "}
                  <strong>
                    "{searchQuery}"
                  </strong>
                </p>

                {/* ==========================================
                    PEOPLE
                ========================================== */}

                {results.users.length > 0 && (

                  <div className="resultSection">

                    <div className="sectionHeading">
                      <h3>
                        👥 People
                      </h3>
                    </div>

                    <div className="userResults">

                      {results.users.map(
                        (user) => (

                          <div
                            className="userResult"
                            key={user.id}
                            onClick={() =>
                              navigate(
                                `/profile/${user.username}`
                              )
                            }
                          >

                            <div className="userAvatar">
                              {user.username
                                .charAt(0)
                                .toUpperCase()}
                            </div>

                            <div className="userInfo">

                              <strong>
                                @{user.username}
                              </strong>

                              {(user.first_name ||
                                user.last_name) && (

                                <span>
                                  {user.first_name}{" "}
                                  {user.last_name}
                                </span>

                              )}

                            </div>

                          </div>

                        )
                      )}

                    </div>

                  </div>

                )}

                {/* ==========================================
                    HASHTAGS
                ========================================== */}

                {results.hashtags.length > 0 && (

                  <div className="resultSection">

                    <div className="sectionHeading">
                      <h3>
                        #️⃣ Hashtags
                      </h3>
                    </div>

                    <div className="hashtagResults">

                      {results.hashtags.map(
                        (hashtag) => (

                          <div
                            className="hashtagResult"
                            key={hashtag.id}
                          >

                            <div className="hashtagIcon">
                              #
                            </div>

                            <div className="hashtagInfo">

                              <strong>
                                #{hashtag.name}
                              </strong>

                              <span>
                                {hashtag.posts_count}{" "}
                                {hashtag.posts_count === 1
                                  ? "post"
                                  : "posts"}
                              </span>

                            </div>

                          </div>

                        )
                      )}

                    </div>

                  </div>

                )}

                {/* ==========================================
                    POSTS
                ========================================== */}

                {results.posts.length > 0 && (

                  <div className="resultSection">

                    <div className="sectionHeading">
                      <h3>
                        📝 Posts
                      </h3>
                    </div>

                    <div className="postResults">

                      {results.posts.map(
                        (post) => (

                          <div
                            className="postResult"
                            key={post.id}
                          >

                            <div className="postHeader">

                              <div className="postAvatar">
                                {post.author.username
                                  .charAt(0)
                                  .toUpperCase()}
                              </div>

                              <strong>
                                @{post.author.username}
                              </strong>

                            </div>

                            <p className="postContent">
                              {post.content}
                            </p>

                            <span className="postDate">
                              {new Date(
                                post.created_at
                              ).toLocaleString()}
                            </span>

                          </div>

                        )
                      )}

                    </div>

                  </div>

                )}

                {/* ==========================================
                    NO RESULTS
                ========================================== */}

                {results.users.length === 0 &&
                  results.posts.length === 0 &&
                  results.hashtags.length === 0 && (

                    <div className="noResults">

                      <div className="noResultsIcon">
                        🔍
                      </div>

                      <h3>
                        No results found
                      </h3>

                      <p>
                        We couldn't find anything
                        matching "{searchQuery}".
                      </p>

                    </div>

                  )}

              </div>

            )}

        </section>

      </main>

    </div>
  );
}
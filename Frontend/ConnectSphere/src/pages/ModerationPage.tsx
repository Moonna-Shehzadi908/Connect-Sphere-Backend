import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./ModerationPage.css";

const API_BASE = "/api/moderation";

/* =========================================================
   TYPES
   ========================================================= */

interface User {
  id: number;
  username: string;
}

interface Post {
  id: number;
  content: string;
  author: string;
}

interface Comment {
  id: number;
  content: string;
  author: string;
}

interface Report {
  id: number;
  reporter: string;
  reason: string;
  status: string;
  created_at: string;
  reviewed_by: string | null;
}

interface ReportDetail {
  id: number;

  reporter: User;

  reported_user: User | null;
  reported_post: Post | null;
  reported_comment: Comment | null;

  reason: string;
  description: string;
  status: string;

  reviewed_by: User | null;

  review_note: string;
  created_at: string;
  reviewed_at: string | null;
}

interface ReportsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Report[];
}

interface Analytics {
  reports_over_time: {
    day: string;
    reports: number;
  }[];

  reports_by_reason: {
    reason: string;
    reports: number;
  }[];

  top_reporters: {
    id: number;
    username: string;
    reports_created: number;
  }[];

  top_moderators: {
    id: number;
    username: string;
    reviews: number;
  }[];

  average_resolution_time: string;
}

/* =========================================================
   COMPONENT
   ========================================================= */

export default function ModerationPage() {
  const navigate = useNavigate();

  const [reports, setReports] = useState<Report[]>([]);
  const [totalReports, setTotalReports] = useState(0);

  const [analytics, setAnalytics] =
    useState<Analytics | null>(null);

  const [selectedReport, setSelectedReport] =
    useState<ReportDetail | null>(null);

  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] =
    useState(false);
  const [actionLoading, setActionLoading] =
    useState(false);

  const [error, setError] = useState("");
  const [actionMessage, setActionMessage] =
    useState("");

  /* =========================================================
     AUTH HELPERS
     ========================================================= */

  const getToken = () => {
    return (
      localStorage.getItem("access") ||
      localStorage.getItem("access_token") ||
      localStorage.getItem("token") ||
      ""
    );
  };

  const getHeaders = (): HeadersInit => {
    const token = getToken();

    return {
      "Content-Type": "application/json",

      ...(token
        ? {
            Authorization: `Bearer ${token}`,
          }
        : {}),
    };
  };

  const handleUnauthorized = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("access_token");
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    navigate("/signin");
  };

  /* =========================================================
     HELPERS
     ========================================================= */

  const getReasonLabel = (
    reason?: string | null
  ) => {
    if (!reason) {
      return "Unknown";
    }

    return String(reason)
      .replaceAll("_", " ")
      .replace(/\b\w/g, (char) =>
        char.toUpperCase()
      );
  };

  const getStatusClass = (
    status?: string | null
  ) => {
    const normalized = String(
      status || ""
    ).toLowerCase();

    if (normalized === "pending") {
      return "status pending";
    }

    if (normalized === "resolved") {
      return "status resolved";
    }

    if (normalized === "rejected") {
      return "status rejected";
    }

    return "status";
  };

  const getReportTarget = (
    report: ReportDetail
  ) => {
    if (report.reported_post) {
      return "Post";
    }

    if (report.reported_comment) {
      return "Comment";
    }

    if (report.reported_user) {
      return "User";
    }

    return "Content";
  };

  const formatDate = (
    date?: string | null
  ) => {
    if (!date) {
      return "Unknown";
    }

    const parsedDate = new Date(date);

    if (
      Number.isNaN(
        parsedDate.getTime()
      )
    ) {
      return date;
    }

    return parsedDate.toLocaleString();
  };

  /* =========================================================
     FETCH REPORTS
     ========================================================= */

  const fetchReports = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        `${API_BASE}/reports/`,
        {
          method: "GET",
          headers: getHeaders(),
        }
      );

      if (response.status === 401) {
        handleUnauthorized();
        return;
      }

      if (!response.ok) {
        throw new Error(
          "Unable to load moderation reports."
        );
      }

      const data = await response.json();

      /*
       * Backend uses DRF pagination:
       *
       * {
       *   count: 10,
       *   next: "...",
       *   previous: null,
       *   results: [...]
       * }
       *
       * Also supports direct array
       * just in case pagination changes.
       */

      if (Array.isArray(data)) {
        setReports(data);
        setTotalReports(data.length);
      } else {
        const reportData =
          Array.isArray(data?.results)
            ? data.results
            : [];

        setReports(reportData);

        setTotalReports(
          typeof data?.count === "number"
            ? data.count
            : reportData.length
        );
      }
    } catch (err) {
      console.error(
        "Reports error:",
        err
      );

      setError(
        err instanceof Error
          ? err.message
          : "Failed to load reports. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  /* =========================================================
     FETCH ANALYTICS
     ========================================================= */

  const fetchAnalytics = async () => {
    try {
      const response = await fetch(
        `${API_BASE}/analytics/`,
        {
          method: "GET",
          headers: getHeaders(),
        }
      );

      if (response.status === 401) {
        handleUnauthorized();
        return;
      }

      if (!response.ok) {
        console.error(
          "Analytics request failed:",
          response.status
        );

        return;
      }

      const data: Analytics =
        await response.json();

      setAnalytics(data);
    } catch (err) {
      console.error(
        "Analytics error:",
        err
      );
    }
  };

  /* =========================================================
     FETCH EVERYTHING
     ========================================================= */

  const fetchAllData = async () => {
    setActionMessage("");

    await Promise.all([
      fetchReports(),
      fetchAnalytics(),
    ]);
  };

  /* =========================================================
     INITIAL LOAD
     ========================================================= */

  useEffect(() => {
    fetchAllData();
  }, []);

  /* =========================================================
     VIEW REPORT DETAILS
     ========================================================= */

  const handleViewReport = async (
    reportId: number
  ) => {
    try {
      setDetailLoading(true);
      setError("");
      setActionMessage("");

      const response = await fetch(
        `${API_BASE}/reports/${reportId}/`,
        {
          method: "GET",
          headers: getHeaders(),
        }
      );

      if (response.status === 401) {
        handleUnauthorized();
        return;
      }

      if (!response.ok) {
        throw new Error(
          "Unable to load report details."
        );
      }

      const data: ReportDetail =
        await response.json();

      setSelectedReport(data);
    } catch (err) {
      console.error(
        "Report detail error:",
        err
      );

      setError(
        err instanceof Error
          ? err.message
          : "Failed to load report details."
      );
    } finally {
      setDetailLoading(false);
    }
  };

  /* =========================================================
     MODERATION ACTION
     ========================================================= */

  const handleModerationAction = async (
    reportId: number,
    action: string
  ) => {
    try {
      setActionLoading(true);
      setActionMessage("");
      setError("");

      const response = await fetch(
        `${API_BASE}/reports/${reportId}/action/`,
        {
          method: "POST",
          headers: getHeaders(),

          body: JSON.stringify({
            action,
          }),
        }
      );

      if (response.status === 401) {
        handleUnauthorized();
        return;
      }

      const data = await response
        .json()
        .catch(() => null);

      if (!response.ok) {
        throw new Error(
          data?.detail ||
            data?.message ||
            "Moderation action failed."
        );
      }

      setActionMessage(
        data?.message ||
          "Moderation action completed successfully."
      );

      await Promise.all([
        fetchReports(),
        fetchAnalytics(),
      ]);

      if (
        selectedReport?.id === reportId
      ) {
        await handleViewReport(
          reportId
        );
      }
    } catch (err) {
      console.error(
        "Moderation action error:",
        err
      );

      setError(
        err instanceof Error
          ? err.message
          : "Moderation action failed."
      );
    } finally {
      setActionLoading(false);
    }
  };

  /* =========================================================
     LOGOUT
     ========================================================= */

  const handleLogout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("access");
    localStorage.removeItem("access_token");
    localStorage.removeItem("token");

    navigate("/signin");
  };

  /* =========================================================
     STATS
     ========================================================= */

  const pendingReports = useMemo(() => {
    return reports.filter(
      (report) =>
        String(
          report.status || ""
        ).toLowerCase() ===
        "pending"
    ).length;
  }, [reports]);

  const resolvedReports = useMemo(() => {
    return reports.filter(
      (report) =>
        String(
          report.status || ""
        ).toLowerCase() ===
        "resolved"
    ).length;
  }, [reports]);

  const rejectedReports = useMemo(() => {
    return reports.filter(
      (report) =>
        String(
          report.status || ""
        ).toLowerCase() ===
        "rejected"
    ).length;
  }, [reports]);

  /* =========================================================
     CLOSE MODAL
     ========================================================= */

  const handleCloseModal = () => {
    if (actionLoading) {
      return;
    }

    setSelectedReport(null);
  };

  /* =========================================================
     UI
     ========================================================= */

  return (
    <div className="moderationPage">

      {/* =====================================================
          SIDEBAR
          ===================================================== */}

      <aside className="sidebar">

        <div className="sidebarHeader">

          <h2 className="logo">
            ConnectSphere
          </h2>

          <span className="moderatorBadge">
            Moderator
          </span>

        </div>

        <nav className="sidebarNav">

          <button
            type="button"
            className="navItem"
            onClick={() =>
              navigate("/home")
            }
          >
            <span>📄</span>
            Feed
          </button>

          <button
            type="button"
            className="navItem"
            onClick={() =>
              navigate("/messages")
            }
          >
            <span>💬</span>
            Messaging
          </button>

         

          <button
            type="button"
            className="navItem active"
          >
            <span>🛡️</span>
            Moderation
          </button>

        </nav>

        <div className="sidebarBottom">

          <button
            type="button"
            className="createBtn"
            onClick={() =>
              navigate(
                "/create-post"
              )
            }
          >
            + Create Post
          </button>

     <button
  type="button"
  onClick={() => navigate("/home")}
  style={{
    display: "flex",
    visibility: "visible",
    opacity: 1,
    position: "relative",
    zIndex: 9999,

    width: "100%",
    height: "40px",
    minHeight: "40px",

    alignItems: "center",
    justifyContent: "center",

    margin: "0",
    padding: "0 13px",

    backgroundColor: "#4f46e5",
    color: "#ffffff",

    border: "none",
    borderRadius: "9px",

    fontFamily: "inherit",
    fontSize: "13px",
    fontWeight: 700,

    cursor: "pointer",
    boxSizing: "border-box",
  }}
>
  ← Back to Home
</button>

          <button
            type="button"
            className="logoutBtn"
            onClick={handleLogout}
          >
            Logout
          </button>

        </div>

      </aside>

      {/* =====================================================
          MAIN AREA
          ===================================================== */}

      <main className="mainArea">

        {/* ===================================================
            HEADER
            =================================================== */}

        <div className="topBar">

          <div>

            <p className="pageLabel">
              CONTENT SAFETY
            </p>

            <h1>
              Moderation Dashboard
            </h1>

            <p className="pageDescription">
              Review reports and take moderation
              actions across ConnectSphere.
            </p>

          </div>

          <button
            type="button"
            className="refreshBtn"
            onClick={fetchAllData}
            disabled={loading}
          >
            ↻ Refresh
          </button>

        </div>

        {/* ===================================================
            MESSAGES
            =================================================== */}

        {error && (
          <div className="errorMessage">
            {error}
          </div>
        )}

        {actionMessage && (
          <div className="successMessage">
            {actionMessage}
          </div>
        )}

        {/* ===================================================
            STATS
            =================================================== */}

        <section className="stats">

          <div className="statCard">

            <div className="statIcon pendingIcon">
              ⏳
            </div>

            <div>
              <span>
                Pending Reports
              </span>

              <strong>
                {pendingReports}
              </strong>
            </div>

          </div>

          <div className="statCard">

            <div className="statIcon resolvedIcon">
              ✓
            </div>

            <div>
              <span>
                Resolved
              </span>

              <strong>
                {resolvedReports}
              </strong>
            </div>

          </div>

          <div className="statCard">

            <div className="statIcon rejectedIcon">
              !
            </div>

            <div>
              <span>
                Rejected
              </span>

              <strong>
                {rejectedReports}
              </strong>
            </div>

          </div>

          <div className="statCard">

            <div className="statIcon totalIcon">
              #
            </div>

            <div>
              <span>
                Total Reports
              </span>

              <strong>
                {totalReports}
              </strong>
            </div>

          </div>

        </section>

        {/* ===================================================
            REPORTS
            =================================================== */}

        <section className="reportSection">

          <div className="sectionHeader">

            <div>

              <h2>
                Reported Content
              </h2>

              <p>
                Review user-submitted reports and
                moderation requests.
              </p>

            </div>

            <span className="reportCount">
              {totalReports}{" "}
              {totalReports === 1
                ? "Report"
                : "Reports"}
            </span>

          </div>

          {loading ? (

            <div className="emptyState">

              <div className="loader"></div>

              <p>
                Loading moderation reports...
              </p>

            </div>

          ) : reports.length === 0 ? (

            <div className="emptyState">

              <div className="emptyIcon">
                ✓
              </div>

              <h3>
                No reports found
              </h3>

              <p>
                There are currently no moderation
                reports to review.
              </p>

            </div>

          ) : (

            <div className="reportsList">

              {reports.map(
                (report) => (

                  <div
                    key={report.id}
                    className="reportCard"
                  >

                    <div className="reportMain">

                      <div className="reportIcon">
                        🛡️
                      </div>

                      <div className="reportInfo">

                        <div className="reportTitleRow">

                          <h3>
                            Report #{report.id}
                          </h3>

                          <span
                            className={getStatusClass(
                              report.status
                            )}
                          >
                            {getReasonLabel(
                              report.status
                            )}
                          </span>

                        </div>

                        <p className="reportReason">
                          {getReasonLabel(
                            report.reason
                          )}
                        </p>

                        <div className="reportMeta">

                          <span>
                            Reporter:{" "}
                            <strong>
                              {report.reporter ||
                                "Unknown"}
                            </strong>
                          </span>

                          <span>
                            •
                          </span>

                          <span>
                            {formatDate(
                              report.created_at
                            )}
                          </span>

                        </div>

                      </div>

                    </div>

                    <button
                      type="button"
                      className="viewBtn"
                      onClick={() =>
                        handleViewReport(
                          report.id
                        )
                      }
                    >
                      View Details →
                    </button>

                  </div>

                )
              )}

            </div>

          )}

        </section>

        {/* ===================================================
            ANALYTICS
            =================================================== */}

        {analytics && (

          <section className="analyticsSection">

            <div className="sectionHeader">

              <div>

                <h2>
                  Moderation Insights
                </h2>

                <p>
                  Data provided by the moderation
                  analytics API.
                </p>

              </div>

            </div>

            <div className="analyticsGrid">

              <div className="analyticsCard">

                <span>
                  Resolution Time
                </span>

                <strong>
                  {analytics.average_resolution_time ||
                    "No data"}
                </strong>

              </div>

              <div className="analyticsCard">

                <span>
                  Most Reported Reason
                </span>

                <strong>
                  {analytics.reports_by_reason
                    ?.length
                    ? getReasonLabel(
                        analytics
                          .reports_by_reason[0]
                          .reason
                      )
                    : "No data"}
                </strong>

              </div>

              <div className="analyticsCard">

                <span>
                  Top Reporter
                </span>

                <strong>
                  {analytics.top_reporters
                    ?.length
                    ? analytics
                        .top_reporters[0]
                        .username
                    : "No data"}
                </strong>

              </div>

              <div className="analyticsCard">

                <span>
                  Top Moderator
                </span>

                <strong>
                  {analytics.top_moderators
                    ?.length
                    ? analytics
                        .top_moderators[0]
                        .username
                    : "No data"}
                </strong>

              </div>

            </div>

          </section>

        )}

      </main>

      {/* =====================================================
          REPORT DETAIL MODAL
          ===================================================== */}

      {(selectedReport ||
        detailLoading) && (

        <div
          className="modalOverlay"
          onClick={handleCloseModal}
        >

          <div
            className="reportModal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            {detailLoading ? (

              <div className="modalLoading">

                <div className="loader"></div>

                <p>
                  Loading report details...
                </p>

              </div>

            ) : selectedReport ? (

              <>

                {/* =================================================
                    MODAL HEADER
                    ================================================= */}

                <div className="modalHeader">

                  <div>

                    <p className="pageLabel">
                      MODERATION REPORT
                    </p>

                    <h2>
                      Report #
                      {selectedReport.id}
                    </h2>

                  </div>

                  <button
                    type="button"
                    className="closeBtn"
                    onClick={
                      handleCloseModal
                    }
                    disabled={
                      actionLoading
                    }
                    aria-label="Close report"
                  >
                    ×
                  </button>

                </div>

                {/* =================================================
                    STATUS
                    ================================================= */}

                <div className="detailStatusRow">

                  <span
                    className={getStatusClass(
                      selectedReport.status
                    )}
                  >
                    {getReasonLabel(
                      selectedReport.status
                    )}
                  </span>

                  <span className="targetBadge">
                    {getReportTarget(
                      selectedReport
                    )}
                  </span>

                </div>

                {/* =================================================
                    DETAILS
                    ================================================= */}

                <div className="detailGrid">

                  <div className="detailItem">

                    <span>
                      Reporter
                    </span>

                    <strong>
                      {selectedReport.reporter
                        ?.username ||
                        "Unknown"}
                    </strong>

                  </div>

                  <div className="detailItem">

                    <span>
                      Reason
                    </span>

                    <strong>
                      {getReasonLabel(
                        selectedReport.reason
                      )}
                    </strong>

                  </div>

                  <div className="detailItem">

                    <span>
                      Created
                    </span>

                    <strong>
                      {formatDate(
                        selectedReport.created_at
                      )}
                    </strong>

                  </div>

                  <div className="detailItem">

                    <span>
                      Reviewed By
                    </span>

                    <strong>
                      {selectedReport.reviewed_by
                        ?.username ||
                        "Not reviewed"}
                    </strong>

                  </div>

                </div>

                {/* =================================================
                    DESCRIPTION
                    ================================================= */}

                <div className="detailBlock">

                  <h3>
                    Description
                  </h3>

                  <p>
                    {selectedReport.description ||
                      "No additional description provided."}
                  </p>

                </div>

                {/* =================================================
                    REVIEW NOTE
                    ================================================= */}

                {selectedReport.review_note && (

                  <div className="detailBlock">

                    <h3>
                      Review Note
                    </h3>

                    <p>
                      {
                        selectedReport.review_note
                      }
                    </p>

                  </div>

                )}

                {/* =================================================
                    REVIEWED AT
                    ================================================= */}

                {selectedReport.reviewed_at && (

                  <div className="detailBlock">

                    <h3>
                      Reviewed At
                    </h3>

                    <p>
                      {formatDate(
                        selectedReport.reviewed_at
                      )}
                    </p>

                  </div>

                )}

                {/* =================================================
                    REPORTED USER
                    ================================================= */}

                {selectedReport.reported_user && (

                  <div className="targetBlock">

                    <span className="targetBlockLabel">
                      Reported User
                    </span>

                    <strong>
                      @
                      {
                        selectedReport
                          .reported_user
                          .username
                      }
                    </strong>

                  </div>

                )}

                {/* =================================================
                    REPORTED POST
                    ================================================= */}

                {selectedReport.reported_post && (

                  <div className="contentPreview">

                    <div className="contentPreviewHeader">

                      <span>
                        Reported Post
                      </span>

                      <small>
                        Post #
                        {
                          selectedReport
                            .reported_post
                            .id
                        }
                      </small>

                    </div>

                    <p>
                      {
                        selectedReport
                          .reported_post
                          .content ||
                        "No post content available."
                      }
                    </p>

                    <small>
                      Author:{" "}
                      {
                        selectedReport
                          .reported_post
                          .author ||
                        "Unknown"
                      }
                    </small>

                  </div>

                )}

                {/* =================================================
                    REPORTED COMMENT
                    ================================================= */}

                {selectedReport.reported_comment && (

                  <div className="contentPreview">

                    <div className="contentPreviewHeader">

                      <span>
                        Reported Comment
                      </span>

                      <small>
                        Comment #
                        {
                          selectedReport
                            .reported_comment
                            .id
                        }
                      </small>

                    </div>

                    <p>
                      {
                        selectedReport
                          .reported_comment
                          .content ||
                        "No comment content available."
                      }
                    </p>

                    <small>
                      Author:{" "}
                      {
                        selectedReport
                          .reported_comment
                          .author ||
                        "Unknown"
                      }
                    </small>

                  </div>

                )}

                {/* =================================================
                    MODERATION ACTIONS
                    ================================================= */}

                {String(
                  selectedReport.status ||
                    ""
                ).toLowerCase() ===
                  "pending" && (

                  <div className="moderationActions">

                    <h3>
                      Moderation Actions
                    </h3>

                    <div className="actionButtons">

                      {/* Remove Post */}

                      {selectedReport.reported_post && (

                        <button
                          type="button"
                          className="dangerAction"
                          disabled={
                            actionLoading
                          }
                          onClick={() =>
                            handleModerationAction(
                              selectedReport.id,
                              "remove_post"
                            )
                          }
                        >
                          Remove Post
                        </button>

                      )}

                      {/* Remove Comment */}

                      {selectedReport.reported_comment && (

                        <button
                          type="button"
                          className="dangerAction"
                          disabled={
                            actionLoading
                          }
                          onClick={() =>
                            handleModerationAction(
                              selectedReport.id,
                              "remove_comment"
                            )
                          }
                        >
                          Remove Comment
                        </button>

                      )}

                      {/* Warn User */}

                      {(
                        selectedReport
                          .reported_user ||
                        selectedReport
                          .reported_post ||
                        selectedReport
                          .reported_comment
                      ) && (

                        <button
                          type="button"
                          className="warningAction"
                          disabled={
                            actionLoading
                          }
                          onClick={() =>
                            handleModerationAction(
                              selectedReport.id,
                              "warn_user"
                            )
                          }
                        >
                          Warn User
                        </button>

                      )}

                      {/* Suspend User */}

                      {selectedReport.reported_user && (

                        <button
                          type="button"
                          className="suspendAction"
                          disabled={
                            actionLoading
                          }
                          onClick={() =>
                            handleModerationAction(
                              selectedReport.id,
                              "suspend_user"
                            )
                          }
                        >
                          Suspend User
                        </button>

                      )}

                    </div>

                    {actionLoading && (

                      <p className="actionLoadingText">
                        Processing moderation action...
                      </p>

                    )}

                  </div>

                )}

              </>

            ) : null}

          </div>

        </div>

      )}

    </div>
  );
}
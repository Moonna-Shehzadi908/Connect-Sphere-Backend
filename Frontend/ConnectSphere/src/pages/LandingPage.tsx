import { useState } from "react";
import "./LandingPage.css";

import heroImage from "../assets/landingpage.webp";
import feature1 from "../assets/emplyee.webp";
import feature2 from "../assets/mbl.webp";

import { useNavigate } from "react-router-dom";

export default function LandingPage() {
  const navigate = useNavigate();

  const [menuOpen, setMenuOpen] = useState(false);

  /*
   * Check whether user is logged in.
   * Your existing login system stores the user in localStorage.
   */
  const isLoggedIn = () => {
    const user = localStorage.getItem("user");
    return !!user;
  };

  /*
   * Protected actions
   *
   * User must sign in before accessing the actual
   * ConnectSphere application.
   */
  const requireLogin = (path: string) => {
    if (!isLoggedIn()) {
      alert("Please Sign In or create an account first to access ConnectSphere.");
      navigate("/signin");
      return;
    }

    navigate(path);
  };

  /*
   * Scroll to landing-page sections
   */
  const scrollToSection = (id: string) => {
    document.getElementById(id)?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });

    setMenuOpen(false);
  };

  /*
   * Close menu
   */
  const closeMenu = () => {
    setMenuOpen(false);
  };

  return (
    <div className="page">

      {/* =====================================================
          TOP HEADER
      ===================================================== */}
      <header className="topHeader">

        {/* MENU BUTTON */}
        <button
          className={`menu ${menuOpen ? "menuActive" : ""}`}
          onClick={() => setMenuOpen((prev) => !prev)}
          aria-label="Open navigation menu"
          aria-expanded={menuOpen}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        {/* PAGE TITLE */}
        <h1 className="title">
          ConnectSphere Social Hub
        </h1>

        {/* SIGN IN */}
        <button
          className="signBtn"
          onClick={() => navigate("/signin")}
        >
          Sign In
        </button>

      </header>


      {/* =====================================================
          VERTICAL DROPDOWN MENU
      ===================================================== */}
      {menuOpen && (
        <>
          <div
            className="menuBackdrop"
            onClick={closeMenu}
          />

          <div className="landingMenu">

            <button
              onClick={() => {
                closeMenu();
                window.scrollTo({
                  top: 0,
                  behavior: "smooth",
                });
              }}
            >
              <span>🏠</span>
              Home
            </button>

            <button
              onClick={() => scrollToSection("features")}
            >
              <span>✨</span>
              Features
            </button>

            <button
              onClick={() => {
                closeMenu();
                requireLogin("/home");
              }}
            >
              <span>👥</span>
              Community
            </button>

            <button
              onClick={() => scrollToSection("about")}
            >
              <span>ℹ️</span>
              About
            </button>

            <button
              onClick={() => {
                closeMenu();
                navigate("/signin");
              }}
            >
              <span>🔐</span>
              Sign In
            </button>

          </div>
        </>
      )}


      {/* =====================================================
          MAIN CARD
      ===================================================== */}
      <section className="card">

        {/* ===================================================
            NAVBAR
        =================================================== */}
        <div className="navBar">

          {/* LOGO */}
          <button
            className="logo"
            onClick={() => {
              window.scrollTo({
                top: 0,
                behavior: "smooth",
              });
            }}
          >
            ConnectSphere
          </button>


          {/* NAV LINKS */}
          <nav className="navLinks">

            <button
              className="navBtn"
              onClick={() => {
                window.scrollTo({
                  top: 0,
                  behavior: "smooth",
                });
              }}
            >
              Home
            </button>

            <button
              className="navBtn"
              onClick={() => scrollToSection("features")}
            >
              Features
            </button>

            <button
              className="navBtn"
              onClick={() => requireLogin("/home")}
            >
              Community
            </button>

            <button
              className="navBtn"
              onClick={() => scrollToSection("about")}
            >
              About
            </button>
            

          </nav>


          {/* HEADER ICONS */}
          <div className="icons">
              {/* SEARCH */}

            <button
    className="iconBtn"
    onClick={() => requireLogin("/search")}
    title="Search"
    aria-label="Search"
  >
    🔍
  </button>

            {/* NOTIFICATIONS */}
            <button
              className="iconBtn"
              onClick={() => requireLogin("/notifications")}
              title="Notifications"
              aria-label="Notifications"
            >
              🔔
            </button>

            {/* MESSAGES */}
            <button
              className="iconBtn"
              onClick={() => requireLogin("/messages")}
              title="Messages"
              aria-label="Messages"
            >
              ✉️
            </button>

            {/* PROFILE */}
            <button
              className="iconBtn"
              onClick={() => requireLogin("/profile")}
              title="Profile"
              aria-label="Profile"
            >
              👤
            </button>

          </div>

        </div>


        {/* =====================================================
            HERO
        ===================================================== */}
        <div className="heroText">

          <div className="heroBadge">
            ✦ Connect. Create. Grow.
          </div>

          <h2>
            Where Creative Minds
            <br />
            <span>Collide and Grow.</span>
          </h2>

          <p>
            ConnectSphere is a next-generation social ecosystem
            for creators, leaders, and innovators.
          </p>


          <div className="buttons">

            {/* JOIN NETWORK */}
            <button
              className="primaryBtn"
              onClick={() => requireLogin("/home")}
            >
              Join The Network
              <span>→</span>
            </button>


            {/* EXPLORE COMMUNITIES */}
            <button
              className="secondaryBtn"
              onClick={() => requireLogin("/home")}
            >
              Explore Communities
              <span>→</span>
            </button>

          </div>

        </div>


        {/* =====================================================
            HERO IMAGE
        ===================================================== */}
        <div className="imageBox">

          <img
            src={heroImage}
            alt="ConnectSphere community"
          />

          <div className="floatingCard">

            <div className="liveIcon">
              ⚡
            </div>

            <div>
              <strong>
                Live Connection
              </strong>

              <p>
                2.6k users active right now
              </p>
            </div>

          </div>

        </div>


        {/* =====================================================
            ABOUT / INTRO
        ===================================================== */}
        <div
          className="bottom"
          id="about"
        >

          <div className="sectionLine"></div>

          <h3>
            Designed for Impact
          </h3>

          <p>
            Modern tools for modern creators & professionals
          </p>

        </div>

      </section>


      {/* =====================================================
          FEATURES
      ===================================================== */}
      <section
        className="featuresSection"
        id="features"
      >

        {/* FEATURE 1 */}
        <div className="featureCard">

          <div className="featureIcon">
            ✦
          </div>

          <h4>
            Infinite Connections
          </h4>

          <p>
            Expand your network.
          </p>

        </div>


        {/* FEATURE IMAGE */}
        <div className="featureImage">

          <img
            src={feature1}
            alt="ConnectSphere connections"
          />

        </div>


        {/* FEATURE 2 */}
        <div className="featureCard purple">

          <div className="featureIcon">
            ✦
          </div>

          <h4>
            Unified Growth
          </h4>

          <p>
            Collaborate on one platform.
          </p>

        </div>


        {/* FEATURE 3 */}
        <div className="featureCard">

          <div className="featureIcon">
            ▣
          </div>

          <h4>
            Precision Analytics
          </h4>

          <p>
            Track engagement in real time.
          </p>

        </div>


        {/* FEATURE IMAGE */}
        <div className="featureImage">

          <img
            src={feature2}
            alt="ConnectSphere analytics"
          />

        </div>


        {/* FEATURE 4 */}
        <div className="featureCard">

          <div className="featureIcon">
            ↗
          </div>

          <h4>
            Exponential Growth
          </h4>

          <p>
            Unlock opportunities.
          </p>

        </div>

      </section>


      {/* =====================================================
          CTA
      ===================================================== */}
      <section
        className="ctaSection"
        id="cta"
      >

        <div className="ctaContent">

          <span className="ctaBadge">
            ✦ START YOUR JOURNEY
          </span>

          <h2>
            Ready to scale your influence?
          </h2>

          <p>
            Join ConnectSphere today.
          </p>

          <button
            className="primaryBtn ctaButton"
            onClick={() => navigate("/signup")}
          >
            Get Started Now
            <span>→</span>
          </button>

        </div>

      </section>

    </div>
  );
}
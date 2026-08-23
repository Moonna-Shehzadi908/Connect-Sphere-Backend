import { Routes, Route } from "react-router-dom";

import LandingPage from "../pages/LandingPage";
import HomeFeed from "../pages/HomeFeed";
import SignUpPage from "../pages/SignUpPage";
import SignInPage from "../pages/SignInPage";
import MessagesPage from "../pages/MessagesPage";
import ModerationPage from "../pages/ModerationPage";
import CreatePostPage from "../pages/CreatePostPage";
import ProfilePage from "../pages/ProfilePage";
import Notifications from "../pages/Notifications";
import SearchPage from "../pages/SearchPage";
export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/home" element={<HomeFeed />} />
      <Route path="/signup" element={<SignUpPage />} />
      <Route path="/signin" element={<SignInPage />} />
      <Route path="/messages" element={<MessagesPage />} />
      <Route path="/moderation" element={<ModerationPage />} />
      <Route path="/create-post" element={<CreatePostPage />} />
      <Route path="/search" element={<SearchPage />} />
      <Route
  path="/notifications"
  element={<Notifications />}
/>

<Route
    path="/profile"
    element={<ProfilePage />}
/>
    </Routes>
  );
}
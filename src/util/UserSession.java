package util;

import model.User;

/**
 * Manages the current authenticated user session in memory.
 */
public final class UserSession {

    private static User currentUser;

    private UserSession() {
    }

    public static void login(User user) {
        currentUser = user;
    }

    public static void logout() {
        currentUser = null;
    }

    public static User getCurrentUser() {
        return currentUser;
    }

    public static boolean isLoggedIn() {
        return currentUser != null;
    }

    public static boolean isAdmin() {
        return currentUser != null && currentUser.isAdmin();
    }

    public static boolean isCustomer() {
        return currentUser != null && currentUser.isCustomer();
    }
}

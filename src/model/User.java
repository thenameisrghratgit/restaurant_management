package model;

/**
 * Represents an authenticated system user (Admin or Customer).
 */
public class User {

    public static final String ROLE_ADMIN = "ADMIN";
    public static final String ROLE_CUSTOMER = "CUSTOMER";

    private int userId;
    private String username;
    private String fullName;
    private String phone;
    private String email;
    private String role;
    private Integer customerId; // null for pure admins, set for registered customers

    public User() {
    }

    public User(int userId, String username, String fullName, String phone,
                String email, String role, Integer customerId) {
        this.userId = userId;
        this.username = username;
        this.fullName = fullName;
        this.phone = phone;
        this.email = email;
        this.role = role;
        this.customerId = customerId;
    }

    public User(String username, String fullName, String phone,
                String email, String role, Integer customerId) {
        this.username = username;
        this.fullName = fullName;
        this.phone = phone;
        this.email = email;
        this.role = role;
        this.customerId = customerId;
    }

    public boolean isAdmin() {
        return ROLE_ADMIN.equalsIgnoreCase(role);
    }

    public boolean isCustomer() {
        return ROLE_CUSTOMER.equalsIgnoreCase(role);
    }

    // ----- Getters & Setters -----

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public Integer getCustomerId() {
        return customerId;
    }

    public void setCustomerId(Integer customerId) {
        this.customerId = customerId;
    }

    @Override
    public String toString() {
        return fullName + " (" + role + ")";
    }
}

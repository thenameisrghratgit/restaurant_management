package gui;

import model.User;
import util.DBConnection;
import util.UserSession;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.sql.Connection;

/**
 * Main application window.
 * Flow: Auth (Sign In / Register) -> Admin Dashboard / Customer Dashboard.
 */
public class MainFrame extends JFrame {

    private final CardLayout cardLayout = new CardLayout();
    private final JPanel cardsPanel = new JPanel(cardLayout);

    // Panels
    private AuthPanel authPanel;
    private AdminDashboardPanel adminDashboardPanel;
    private CustomerDashboardPanel customerDashboardPanel;

    // Top Navigation Bar
    private final JPanel navBar = new JPanel(new BorderLayout());
    private final JLabel brandLabel = new JLabel("  Restaurant Table Reservation System");
    private final JPanel navRightPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
    private final JLabel userBadgeLabel = new JLabel("");
    private final JButton logoutBtn = GUITheme.button("Logout", GUITheme.DANGER);

    // Bottom Status Bar
    private final JLabel dbStatusLabel = new JLabel("Checking database...");

    private String currentView = "AUTH";

    public MainFrame() {
        setTitle("Restaurant Table Reservation System");
        setSize(1080, 720);
        setMinimumSize(new Dimension(900, 620));
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        initComponents();

        add(navBar, BorderLayout.NORTH);
        add(cardsPanel, BorderLayout.CENTER);
        add(buildStatusBar(), BorderLayout.SOUTH);

        showView("AUTH");
        refreshDatabaseStatus();
    }

    private void initComponents() {
        buildNavBar();

        // 1. Auth Panel (Login + Register)
        authPanel = new AuthPanel((user, targetView) -> showView(targetView));

        // 2. Admin Dashboard
        adminDashboardPanel = new AdminDashboardPanel(this);

        // 3. Customer Dashboard
        customerDashboardPanel = new CustomerDashboardPanel(this);

        cardsPanel.add(authPanel, "AUTH");
        cardsPanel.add(adminDashboardPanel, "ADMIN_DASHBOARD");
        cardsPanel.add(customerDashboardPanel, "CUSTOMER_DASHBOARD");
    }

    private void buildNavBar() {
        navBar.setBackground(GUITheme.PRIMARY);
        navBar.setBorder(new EmptyBorder(12, 24, 12, 24));

        brandLabel.setFont(new Font("Segoe UI", Font.BOLD, 17));
        brandLabel.setForeground(Color.WHITE);

        navRightPanel.setOpaque(false);

        logoutBtn.setFont(new Font("Segoe UI", Font.BOLD, 12));
        logoutBtn.setBorder(new EmptyBorder(6, 14, 6, 14));
        logoutBtn.addActionListener(e -> handleLogout());

        navBar.add(brandLabel, BorderLayout.WEST);
        navBar.add(navRightPanel, BorderLayout.EAST);
    }

    public void showView(String viewName) {
        this.currentView = viewName;
        cardLayout.show(cardsPanel, viewName);

        if ("ADMIN_DASHBOARD".equals(viewName)) {
            adminDashboardPanel.refreshAllData();
        } else if ("CUSTOMER_DASHBOARD".equals(viewName)) {
            customerDashboardPanel.initCustomerData();
        }

        updateNavItems();
        refreshDatabaseStatus();
        revalidate();
        repaint();
    }

    private void updateNavItems() {
        navRightPanel.removeAll();
        User currentUser = UserSession.getCurrentUser();

        if (currentUser != null &&
                ("ADMIN_DASHBOARD".equals(currentView) || "CUSTOMER_DASHBOARD".equals(currentView))) {

            userBadgeLabel.setText("Signed in: " + currentUser.getFullName() + "  ");
            userBadgeLabel.setFont(new Font("Segoe UI", Font.PLAIN, 13));
            userBadgeLabel.setForeground(new Color(226, 232, 240));

            JLabel roleBadge = GUITheme.badge(
                    currentUser.getRole(),
                    currentUser.isAdmin() ? new Color(245, 124, 0) : new Color(34, 153, 84),
                    Color.WHITE
            );

            navRightPanel.add(userBadgeLabel);
            navRightPanel.add(roleBadge);
            navRightPanel.add(Box.createHorizontalStrut(12));
            navRightPanel.add(logoutBtn);
        }
        // Nothing on the right side during the login screen

        navRightPanel.revalidate();
        navRightPanel.repaint();
    }

    private void handleLogout() {
        if (GUITheme.confirm(this, "Are you sure you want to sign out?", "Confirm Sign Out")) {
            UserSession.logout();
            showView("AUTH");
        }
    }

    private JPanel buildStatusBar() {
        JPanel bar = new JPanel(new BorderLayout());
        bar.setBackground(GUITheme.CARD);
        bar.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createMatteBorder(1, 0, 0, 0, GUITheme.LINE),
                new EmptyBorder(8, 20, 8, 20)));

        dbStatusLabel.setFont(GUITheme.SMALL);
        bar.add(dbStatusLabel, BorderLayout.WEST);

        JLabel hint = new JLabel("College OOP Java Project  *  Swing & MySQL");
        hint.setFont(GUITheme.SMALL);
        hint.setForeground(GUITheme.MUTED);
        bar.add(hint, BorderLayout.EAST);

        return bar;
    }

    public void refreshDatabaseStatus() {
        try (Connection connection = DBConnection.getConnection()) {
            if (connection.isValid(3)) {
                dbStatusLabel.setForeground(GUITheme.SUCCESS);
                dbStatusLabel.setText("Database: Connected to restaurant_db @ localhost:3306");
            } else {
                dbStatusLabel.setForeground(GUITheme.DANGER);
                dbStatusLabel.setText("Database: Connection is not valid");
            }
        } catch (Exception e) {
            dbStatusLabel.setForeground(GUITheme.DANGER);
            dbStatusLabel.setText("Database: Connection error (" + e.getMessage() + ")");
        }
    }
}

package gui;

import dao.UserDAO;
import model.User;
import util.UserSession;
import util.ValidationUtil;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.sql.SQLException;
import java.util.function.BiConsumer;

/**
 * Authentication panel: Sign In and Customer Registration.
 * Starts with Sign In tab active. No landing/back navigation needed.
 */
public class AuthPanel extends JPanel {

    private final BiConsumer<User, String> onLoginSuccess;
    private final UserDAO userDAO = new UserDAO();

    // Segmented tab switching
    private final CardLayout tabCardLayout = new CardLayout();
    private final JPanel tabCardsPanel = new JPanel(tabCardLayout);
    private JButton signInTabBtn;
    private JButton registerTabBtn;

    // Login Form Components
    private final JTextField loginUsernameField = new JTextField(18);
    private final JPasswordField loginPasswordField = new JPasswordField(18);
    private final JLabel loginErrorLabel = new JLabel(" ");

    // Register Form Components
    private final JTextField regFullNameField = new JTextField(18);
    private final JTextField regUsernameField = new JTextField(18);
    private final JTextField regPhoneField = new JTextField(18);
    private final JTextField regEmailField = new JTextField(18);
    private final JPasswordField regPasswordField = new JPasswordField(18);
    private final JPasswordField regConfirmPasswordField = new JPasswordField(18);
    private final JLabel regErrorLabel = new JLabel(" ");

    private boolean isLoginTabActive = true;

    public AuthPanel(BiConsumer<User, String> onLoginSuccess) {
        this.onLoginSuccess = onLoginSuccess;

        setLayout(new BorderLayout());
        setBackground(GUITheme.BACKGROUND);

        add(buildCenterCard(), BorderLayout.CENTER);
    }

    private JPanel buildCenterCard() {
        JPanel wrapper = new JPanel(new GridBagLayout());
        wrapper.setOpaque(false);
        wrapper.setBackground(GUITheme.BACKGROUND);

        JPanel card = new JPanel(new BorderLayout(0, 16));
        GUITheme.card(card);
        card.setPreferredSize(new Dimension(500, 580));
        card.setMinimumSize(new Dimension(460, 540));

        // Card Header
        JPanel cardHeader = new JPanel(new BorderLayout(0, 12));
        cardHeader.setOpaque(false);

        JPanel titles = new JPanel(new BorderLayout(0, 4));
        titles.setOpaque(false);

        JLabel headTitle = new JLabel("Restaurant Reservation System");
        headTitle.setFont(new Font("Segoe UI", Font.BOLD, 20));
        headTitle.setForeground(GUITheme.TEXT);

        JLabel headSub = new JLabel("Sign in to your account or register as a new customer");
        headSub.setFont(GUITheme.SMALL);
        headSub.setForeground(GUITheme.MUTED);

        titles.add(headTitle, BorderLayout.NORTH);
        titles.add(headSub, BorderLayout.SOUTH);
        cardHeader.add(titles, BorderLayout.NORTH);

        // Segmented Tab Switcher
        JPanel tabSwitcher = new JPanel(new GridLayout(1, 2, 8, 0));
        tabSwitcher.setOpaque(false);

        signInTabBtn = GUITheme.button("Sign In", GUITheme.PRIMARY);
        signInTabBtn.setFont(new Font("Segoe UI", Font.BOLD, 13));
        signInTabBtn.addActionListener(e -> switchToLoginTab());

        registerTabBtn = GUITheme.outlineButton("Create Account", GUITheme.LINE, GUITheme.MUTED);
        registerTabBtn.setFont(new Font("Segoe UI", Font.BOLD, 13));
        registerTabBtn.addActionListener(e -> switchToRegisterTab());

        tabSwitcher.add(signInTabBtn);
        tabSwitcher.add(registerTabBtn);
        cardHeader.add(tabSwitcher, BorderLayout.SOUTH);

        card.add(cardHeader, BorderLayout.NORTH);

        // Tab Forms
        tabCardsPanel.setOpaque(false);
        tabCardsPanel.add(buildLoginTab(), "LOGIN");
        tabCardsPanel.add(buildRegisterTab(), "REGISTER");
        card.add(tabCardsPanel, BorderLayout.CENTER);

        wrapper.add(card);
        return wrapper;
    }

    private void switchToLoginTab() {
        isLoginTabActive = true;
        tabCardLayout.show(tabCardsPanel, "LOGIN");
        updateTabButtonStyles();
    }

    private void switchToRegisterTab() {
        isLoginTabActive = false;
        tabCardLayout.show(tabCardsPanel, "REGISTER");
        updateTabButtonStyles();
    }

    private void updateTabButtonStyles() {
        if (isLoginTabActive) {
            signInTabBtn.setBackground(GUITheme.PRIMARY);
            signInTabBtn.setForeground(Color.WHITE);
        } else {
            signInTabBtn.setBackground(GUITheme.CARD);
            signInTabBtn.setForeground(GUITheme.MUTED);
        }
        if (!isLoginTabActive) {
            registerTabBtn.setBackground(GUITheme.PRIMARY);
            registerTabBtn.setForeground(Color.WHITE);
        } else {
            registerTabBtn.setBackground(GUITheme.CARD);
            registerTabBtn.setForeground(GUITheme.MUTED);
        }
        signInTabBtn.repaint();
        registerTabBtn.repaint();
    }

    // ================================================================
    //  SIGN IN TAB
    // ================================================================

    private JPanel buildLoginTab() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setOpaque(false);
        panel.setBorder(new EmptyBorder(10, 8, 8, 8));

        GridBagConstraints gc = new GridBagConstraints();
        gc.insets = new Insets(6, 6, 6, 6);
        gc.fill = GridBagConstraints.HORIZONTAL;
        gc.anchor = GridBagConstraints.WEST;

        int row = 0;

        gc.gridx = 0; gc.gridy = row++; gc.gridwidth = 2;
        panel.add(GUITheme.label("Username:"), gc);

        gc.gridy = row++;
        GUITheme.styleField(loginUsernameField);
        panel.add(loginUsernameField, gc);

        gc.gridy = row++;
        panel.add(GUITheme.label("Password:"), gc);

        gc.gridy = row++;
        stylePasswordField(loginPasswordField);
        panel.add(loginPasswordField, gc);

        gc.gridy = row++;
        loginErrorLabel.setFont(GUITheme.SMALL);
        loginErrorLabel.setForeground(GUITheme.DANGER);
        panel.add(loginErrorLabel, gc);

        gc.gridy = row++;
        JButton signInBtn = GUITheme.button("Sign In", GUITheme.ACCENT);
        signInBtn.setFont(new Font("Segoe UI", Font.BOLD, 14));
        signInBtn.addActionListener(e -> handleLogin());
        panel.add(signInBtn, gc);

        loginUsernameField.addActionListener(e -> handleLogin());
        loginPasswordField.addActionListener(e -> handleLogin());

        // Demo hint
        gc.gridy = row++;
        JPanel demoBox = new JPanel(new BorderLayout(0, 4));
        demoBox.setBackground(new Color(248, 250, 252));
        demoBox.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(GUITheme.LINE, 1, true),
                new EmptyBorder(10, 14, 10, 14)));

        JLabel demoTitle = new JLabel("DEMO CREDENTIALS");
        demoTitle.setFont(new Font("Segoe UI", Font.BOLD, 11));
        demoTitle.setForeground(GUITheme.MUTED);

        JPanel demoLines = new JPanel(new GridLayout(2, 1, 0, 4));
        demoLines.setOpaque(false);
        JLabel l1 = new JLabel("Admin:    admin  /  admin123");
        l1.setFont(GUITheme.SMALL);
        l1.setForeground(GUITheme.TEXT);
        JLabel l2 = new JLabel("Customer: register via 'Create Account' tab");
        l2.setFont(GUITheme.SMALL);
        l2.setForeground(GUITheme.TEXT);
        demoLines.add(l1);
        demoLines.add(l2);

        demoBox.add(demoTitle, BorderLayout.NORTH);
        demoBox.add(demoLines, BorderLayout.CENTER);
        panel.add(demoBox, gc);

        return panel;
    }

    private void handleLogin() {
        String username = loginUsernameField.getText().trim();
        String password = new String(loginPasswordField.getPassword());

        if (username.isEmpty() || password.isEmpty()) {
            loginErrorLabel.setText("Please enter both username and password.");
            return;
        }

        try {
            User user = userDAO.login(username, password);
            if (user == null) {
                loginErrorLabel.setText("Invalid username or password.");
                loginPasswordField.setText("");
            } else {
                loginErrorLabel.setText(" ");
                UserSession.login(user);
                clearFields();
                if (onLoginSuccess != null) {
                    onLoginSuccess.accept(user, user.isAdmin() ? "ADMIN_DASHBOARD" : "CUSTOMER_DASHBOARD");
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
            loginErrorLabel.setText("Database error: " + e.getMessage());
        }
    }

    // ================================================================
    //  REGISTER TAB
    // ================================================================

    private JPanel buildRegisterTab() {
        JPanel scrollContent = new JPanel(new GridBagLayout());
        scrollContent.setOpaque(false);
        scrollContent.setBorder(new EmptyBorder(8, 6, 8, 6));

        GridBagConstraints gc = new GridBagConstraints();
        gc.insets = new Insets(3, 6, 3, 6);
        gc.fill = GridBagConstraints.HORIZONTAL;
        gc.anchor = GridBagConstraints.WEST;

        int row = 0;

        gc.gridx = 0; gc.gridy = row++; gc.gridwidth = 2;
        scrollContent.add(GUITheme.label("Full Name *:"), gc);
        gc.gridy = row++;
        GUITheme.styleField(regFullNameField);
        scrollContent.add(regFullNameField, gc);

        gc.gridy = row++;
        scrollContent.add(GUITheme.label("Username *:"), gc);
        gc.gridy = row++;
        GUITheme.styleField(regUsernameField);
        scrollContent.add(regUsernameField, gc);

        gc.gridy = row++;
        scrollContent.add(GUITheme.label("Phone Number * (10 digits):"), gc);
        gc.gridy = row++;
        GUITheme.styleField(regPhoneField);
        scrollContent.add(regPhoneField, gc);

        gc.gridy = row++;
        scrollContent.add(GUITheme.label("Email Address:"), gc);
        gc.gridy = row++;
        GUITheme.styleField(regEmailField);
        scrollContent.add(regEmailField, gc);

        gc.gridy = row++;
        scrollContent.add(GUITheme.label("Password *:"), gc);
        gc.gridy = row++;
        stylePasswordField(regPasswordField);
        scrollContent.add(regPasswordField, gc);

        gc.gridy = row++;
        scrollContent.add(GUITheme.label("Confirm Password *:"), gc);
        gc.gridy = row++;
        stylePasswordField(regConfirmPasswordField);
        scrollContent.add(regConfirmPasswordField, gc);

        gc.gridy = row++;
        regErrorLabel.setFont(GUITheme.SMALL);
        regErrorLabel.setForeground(GUITheme.DANGER);
        scrollContent.add(regErrorLabel, gc);

        gc.gridy = row++;
        JButton regBtn = GUITheme.button("Create Account & Sign In", GUITheme.SUCCESS);
        regBtn.setFont(new Font("Segoe UI", Font.BOLD, 13));
        regBtn.addActionListener(e -> handleRegistration());
        scrollContent.add(regBtn, gc);

        JScrollPane scroll = new JScrollPane(scrollContent);
        scroll.setBorder(null);
        scroll.setOpaque(false);
        scroll.getViewport().setOpaque(false);

        JPanel wrapper = new JPanel(new BorderLayout());
        wrapper.setOpaque(false);
        wrapper.add(scroll, BorderLayout.CENTER);
        return wrapper;
    }

    private void stylePasswordField(JPasswordField f) {
        f.setFont(GUITheme.BODY);
        f.setBackground(GUITheme.CARD);
        f.setForeground(GUITheme.TEXT);
        f.setCaretColor(GUITheme.TEXT);
        f.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(GUITheme.LINE, 1, true),
                new EmptyBorder(8, 12, 8, 12)));
    }

    private void handleRegistration() {
        String fullName = regFullNameField.getText().trim();
        String username = regUsernameField.getText().trim();
        String phone    = regPhoneField.getText().trim();
        String email    = regEmailField.getText().trim();
        String pass     = new String(regPasswordField.getPassword());
        String confirm  = new String(regConfirmPasswordField.getPassword());

        if (ValidationUtil.isBlank(fullName)) {
            regErrorLabel.setText("Please enter your full name.");
            return;
        }
        if (ValidationUtil.isBlank(username)) {
            regErrorLabel.setText("Please choose a username.");
            return;
        }
        if (!ValidationUtil.isValidPhone(phone)) {
            regErrorLabel.setText("Enter a valid phone number (10–15 digits).");
            return;
        }
        if (!email.isEmpty() && !ValidationUtil.isValidEmail(email)) {
            regErrorLabel.setText("Enter a valid email address.");
            return;
        }
        if (pass.length() < 4) {
            regErrorLabel.setText("Password must be at least 4 characters.");
            return;
        }
        if (!pass.equals(confirm)) {
            regErrorLabel.setText("Passwords do not match.");
            return;
        }

        try {
            if (userDAO.isUsernameTaken(username)) {
                regErrorLabel.setText("Username '" + username + "' is already taken.");
                return;
            }

            User newUser = userDAO.registerCustomer(fullName, username, phone, email, pass);
            regErrorLabel.setText(" ");
            JOptionPane.showMessageDialog(this,
                    "Account created successfully!\nWelcome, " + fullName + "!",
                    "Registration Successful",
                    JOptionPane.INFORMATION_MESSAGE);

            UserSession.login(newUser);
            clearFields();
            if (onLoginSuccess != null) {
                onLoginSuccess.accept(newUser, "CUSTOMER_DASHBOARD");
            }

        } catch (Exception e) {
            e.printStackTrace();
            regErrorLabel.setText("Error: " + e.getMessage());
        }
    }

    private void clearFields() {
        loginUsernameField.setText("");
        loginPasswordField.setText("");
        loginErrorLabel.setText(" ");

        regFullNameField.setText("");
        regUsernameField.setText("");
        regPhoneField.setText("");
        regEmailField.setText("");
        regPasswordField.setText("");
        regConfirmPasswordField.setText("");
        regErrorLabel.setText(" ");
    }
}

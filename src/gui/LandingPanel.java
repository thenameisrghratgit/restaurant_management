package gui;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.util.function.Consumer;

/**
 * Clean and professional Landing / Welcome screen for the
 * Restaurant Table Reservation System.
 */
public class LandingPanel extends JPanel {

    private final Consumer<String> navigation;

    public LandingPanel(Consumer<String> navigation) {
        this.navigation = navigation;
        setLayout(new BorderLayout());
        setBackground(GUITheme.getBackground());

        add(buildHeroSection(), BorderLayout.NORTH);
        add(buildFeatureCards(), BorderLayout.CENTER);
        add(buildBottomBar(), BorderLayout.SOUTH);

        GUITheme.addThemeListener(this::applyTheme);
    }

    private void applyTheme() {
        setBackground(GUITheme.getBackground());
        repaint();
        revalidate();
    }

    private JPanel buildHeroSection() {
        JPanel hero = new JPanel(new BorderLayout(0, 16));
        hero.setBackground(GUITheme.getPrimary());
        hero.setBorder(new EmptyBorder(40, 50, 40, 50));

        JPanel content = new JPanel();
        content.setLayout(new BoxLayout(content, BoxLayout.Y_AXIS));
        content.setOpaque(false);

        // Badge
        JLabel badge = GUITheme.badge("COLLEGE JAVA OOP PROJECT  *  SWING & JDBC",
                new Color(255, 255, 255, 30), new Color(226, 232, 240));
        badge.setAlignmentX(Component.CENTER_ALIGNMENT);

        // Title
        JLabel title = new JLabel("Restaurant Table Reservation System");
        title.setFont(new Font("Segoe UI", Font.BOLD, 32));
        title.setForeground(Color.WHITE);
        title.setAlignmentX(Component.CENTER_ALIGNMENT);

        // Subtitle
        JLabel subtitle = new JLabel(
                "Experience seamless dining reservations with real-time table slot availability & full booking control");
        subtitle.setFont(new Font("Segoe UI", Font.PLAIN, 15));
        subtitle.setForeground(new Color(203, 213, 225));
        subtitle.setAlignmentX(Component.CENTER_ALIGNMENT);

        // Action Buttons Row
        JPanel btnRow = new JPanel(new FlowLayout(FlowLayout.CENTER, 14, 0));
        btnRow.setOpaque(false);

        JButton getStartedBtn = GUITheme.button("Get Started  ->", GUITheme.getAccent());
        getStartedBtn.setFont(new Font("Segoe UI", Font.BOLD, 15));
        getStartedBtn.setBorder(new EmptyBorder(12, 28, 12, 28));
        getStartedBtn.addActionListener(e -> {
            if (navigation != null) {
                navigation.accept("AUTH");
            }
        });

        JButton aboutBtn = GUITheme.outlineButton("Learn More", Color.WHITE, Color.WHITE);
        aboutBtn.setFont(new Font("Segoe UI", Font.BOLD, 15));
        aboutBtn.setBorder(new EmptyBorder(12, 24, 12, 24));
        aboutBtn.addActionListener(e -> showAboutDialog());

        btnRow.add(getStartedBtn);
        btnRow.add(aboutBtn);

        content.add(badge);
        content.add(Box.createVerticalStrut(14));
        content.add(title);
        content.add(Box.createVerticalStrut(8));
        content.add(subtitle);
        content.add(Box.createVerticalStrut(24));
        content.add(btnRow);

        hero.add(content, BorderLayout.CENTER);
        return hero;
    }

    private JPanel buildFeatureCards() {
        JPanel container = new JPanel(new BorderLayout());
        container.setOpaque(false);
        container.setBorder(new EmptyBorder(30, 40, 20, 40));

        JPanel grid = new JPanel(new GridLayout(1, 3, 20, 0));
        grid.setOpaque(false);

        grid.add(createCard(
                "Real-Time Slot Booking",
                "Lock in reservations by date and time. Built-in conflict prevention ensures no double-booked tables.",
                "Atomic Transactions",
                GUITheme.getAccent()
        ));

        grid.add(createCard(
                "Live Table Availability",
                "Instantly view tables dynamically categorized by party capacity and occupied slots.",
                "Per-Slot Calculation",
                GUITheme.SUCCESS
        ));

        grid.add(createCard(
                "Role-Based Dashboards",
                "Dedicated portals for Dining Customers (book & manage own stays) and Staff Admins (full CRUD & monitoring).",
                "Secure Passwords",
                new Color(59, 130, 246)
        ));

        container.add(grid, BorderLayout.CENTER);
        return container;
    }

    private JPanel createCard(String title, String desc, String tag, Color accent) {
        JPanel card = new JPanel(new BorderLayout(0, 10));
        GUITheme.card(card);

        JLabel tagLabel = new JLabel(tag.toUpperCase());
        tagLabel.setFont(new Font("Segoe UI", Font.BOLD, 11));
        tagLabel.setForeground(accent);

        JLabel titleLabel = new JLabel(title);
        titleLabel.setFont(new Font("Segoe UI", Font.BOLD, 17));
        titleLabel.setForeground(GUITheme.getText());

        JLabel descLabel = new JLabel("<html><body style='width: 170px;'>" + desc + "</body></html>");
        descLabel.setFont(GUITheme.BODY);
        descLabel.setForeground(GUITheme.getMuted());

        JPanel header = new JPanel(new BorderLayout(0, 4));
        header.setOpaque(false);
        header.add(tagLabel, BorderLayout.NORTH);
        header.add(titleLabel, BorderLayout.CENTER);

        card.add(header, BorderLayout.NORTH);
        card.add(descLabel, BorderLayout.CENTER);

        return card;
    }

    private JPanel buildBottomBar() {
        JPanel bar = new JPanel(new BorderLayout());
        bar.setOpaque(false);
        bar.setBorder(new EmptyBorder(12, 40, 20, 40));

        JLabel hint = new JLabel("Ready to book or manage tables? Click 'Get Started' to sign in or register as a guest.");
        hint.setFont(GUITheme.SMALL);
        hint.setForeground(GUITheme.getMuted());

        JLabel creds = new JLabel("Admin Demo: admin / admin123  *  Self-Registration Available");
        creds.setFont(GUITheme.SMALL);
        creds.setForeground(GUITheme.getMuted());

        bar.add(hint, BorderLayout.WEST);
        bar.add(creds, BorderLayout.EAST);
        return bar;
    }

    private void showAboutDialog() {
        JOptionPane.showMessageDialog(this,
                """
                Restaurant Table Reservation System
                Object-Oriented Programming with Java & Swing
                
                Architecture:
                * GUI: Java Swing (Event Dispatch Thread, CardLayout, custom styles)
                * Database: MySQL (restaurant_db) with JDBC Driver 9.x
                * Security: Salted SHA-256 password hashing
                * Transactions: Atomic reservation creation & slot validation
                * Layered MVC: model, dao, gui, util packages
                
                Click 'Get Started' to proceed to the Login and Registration screens.""",
                "About Project", JOptionPane.INFORMATION_MESSAGE);
    }
}

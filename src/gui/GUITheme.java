package gui;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.JTableHeader;
import java.awt.*;
import java.awt.geom.RoundRectangle2D;
import java.util.ArrayList;
import java.util.List;

/**
 * Shared colours, fonts and component factories so that every screen of the
 * application looks consistent. Supports both clean Light and Dark modes.
 */
public final class GUITheme {

    // ----- Light Mode Defaults (Backwards Compatibility) -----
    public static final Color PRIMARY = new Color(34, 43, 54);
    public static final Color PRIMARY_LIGHT = new Color(52, 64, 80);
    public static final Color ACCENT = new Color(196, 88, 34);
    public static final Color ACCENT_DARK = new Color(163, 69, 24);
    public static final Color BACKGROUND = new Color(241, 245, 249);
    public static final Color CARD = Color.WHITE;
    public static final Color TEXT = new Color(30, 41, 59);
    public static final Color MUTED = new Color(100, 116, 139);
    public static final Color SUCCESS = new Color(22, 163, 74);
    public static final Color DANGER = new Color(220, 38, 38);
    public static final Color WARNING = new Color(217, 119, 6);
    public static final Color LINE = new Color(226, 232, 240);
    public static final Color SELECTION = new Color(224, 238, 255);

    // ----- Dark Mode Palette -----
    private static final Color DARK_PRIMARY = new Color(15, 23, 42);
    private static final Color DARK_PRIMARY_LIGHT = new Color(30, 41, 59);
    private static final Color DARK_ACCENT = new Color(234, 88, 12);
    private static final Color DARK_BACKGROUND = new Color(11, 15, 25);
    private static final Color DARK_CARD = new Color(23, 32, 51);
    private static final Color DARK_TEXT = new Color(241, 245, 249);
    private static final Color DARK_MUTED = new Color(148, 163, 184);
    private static final Color DARK_LINE = new Color(51, 65, 85);
    private static final Color DARK_SELECTION = new Color(45, 62, 80);

    // ----- Fonts -----
    public static final Font TITLE = new Font("Segoe UI", Font.BOLD, 26);
    public static final Font SUBTITLE = new Font("Segoe UI", Font.PLAIN, 14);
    public static final Font HEADING = new Font("Segoe UI", Font.BOLD, 16);
    public static final Font SECTION = new Font("Segoe UI", Font.BOLD, 15);
    public static final Font LABEL = new Font("Segoe UI", Font.PLAIN, 13);
    public static final Font BODY = new Font("Segoe UI", Font.PLAIN, 13);
    public static final Font SMALL = new Font("Segoe UI", Font.PLAIN, 12);
    public static final Font BUTTON = new Font("Segoe UI", Font.BOLD, 13);
    public static final Font DASHBOARD_BUTTON = new Font("Segoe UI", Font.BOLD, 15);

    private static boolean darkMode = false;
    private static final List<Runnable> themeListeners = new ArrayList<>();

    private GUITheme() {
        // utility class
    }

    // ================================================================
    //  THEME TOGGLE & STATE
    // ================================================================

    public static boolean isDarkMode() {
        return darkMode;
    }

    public static void setDarkMode(boolean dark) {
        if (darkMode != dark) {
            darkMode = dark;
            notifyListeners();
        }
    }

    public static void toggleDarkMode() {
        setDarkMode(!darkMode);
    }

    public static void addThemeListener(Runnable listener) {
        themeListeners.add(listener);
    }

    private static void notifyListeners() {
        for (Runnable r : themeListeners) {
            try {
                r.run();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    // ================================================================
    //  DYNAMIC COLOR ACCESSORS
    // ================================================================

    public static Color getPrimary() {
        return darkMode ? DARK_PRIMARY : PRIMARY;
    }

    public static Color getPrimaryLight() {
        return darkMode ? DARK_PRIMARY_LIGHT : PRIMARY_LIGHT;
    }

    public static Color getAccent() {
        return darkMode ? DARK_ACCENT : ACCENT;
    }

    public static Color getBackground() {
        return darkMode ? DARK_BACKGROUND : BACKGROUND;
    }

    public static Color getCard() {
        return darkMode ? DARK_CARD : CARD;
    }

    public static Color getText() {
        return darkMode ? DARK_TEXT : TEXT;
    }

    public static Color getMuted() {
        return darkMode ? DARK_MUTED : MUTED;
    }

    public static Color getLine() {
        return darkMode ? DARK_LINE : LINE;
    }

    public static Color getSelection() {
        return darkMode ? DARK_SELECTION : SELECTION;
    }

    // ================================================================
    //  COMPONENT FACTORIES
    // ================================================================

    /**
     * Rounded, flat button with hover and pressed states.
     */
    public static JButton button(String text, Color background) {
        JButton button = new JButton(text) {
            @Override
            protected void paintComponent(Graphics g) {
                Graphics2D g2 = (Graphics2D) g.create();
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                        RenderingHints.VALUE_ANTIALIAS_ON);

                Color base = getBackground();
                if (!isEnabled()) {
                    base = getLine();
                } else if (getModel().isPressed()) {
                    base = base.darker();
                } else if (getModel().isRollover()) {
                    base = base.brighter();
                }

                g2.setColor(base);
                g2.fill(new RoundRectangle2D.Double(0, 0,
                        getWidth() - 1, getHeight() - 1, 10, 10));

                g2.setColor(isEnabled() ? getForeground() : getMuted());
                g2.setFont(getFont());
                FontMetrics fm = g2.getFontMetrics();
                String label = getText();
                int x = (getWidth() - fm.stringWidth(label)) / 2;
                int y = (getHeight() + fm.getAscent() - fm.getDescent()) / 2;
                g2.drawString(label, x, y);
                g2.dispose();
            }
        };

        button.setFont(BUTTON);
        button.setForeground(Color.WHITE);
        button.setBackground(background != null ? background : getPrimary());
        button.setFocusPainted(false);
        button.setRolloverEnabled(true);
        button.setBorder(new EmptyBorder(10, 18, 10, 18));
        button.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        return button;
    }

    /** Large button used on dashboard action tiles. */
    public static JButton dashboardButton(String text, Color background) {
        JButton button = button(text, background);
        button.setFont(DASHBOARD_BUTTON);
        button.setBorder(new EmptyBorder(14, 20, 14, 20));
        return button;
    }

    /** Outlined button with clean rounded border. */
    public static JButton outlineButton(String text, Color borderColor, Color textColor) {
        JButton button = new JButton(text) {
            @Override
            protected void paintComponent(Graphics g) {
                Graphics2D g2 = (Graphics2D) g.create();
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                        RenderingHints.VALUE_ANTIALIAS_ON);

                Color bg = getModel().isRollover()
                        ? (darkMode ? new Color(255, 255, 255, 20) : new Color(0, 0, 0, 10))
                        : new Color(0, 0, 0, 0);

                g2.setColor(bg);
                g2.fill(new RoundRectangle2D.Double(0, 0,
                        getWidth() - 1, getHeight() - 1, 10, 10));

                g2.setColor(borderColor);
                g2.setStroke(new BasicStroke(1.5f));
                g2.draw(new RoundRectangle2D.Double(1, 1,
                        getWidth() - 3, getHeight() - 3, 10, 10));

                g2.setColor(textColor);
                g2.setFont(getFont());
                FontMetrics fm = g2.getFontMetrics();
                String label = getText();
                int x = (getWidth() - fm.stringWidth(label)) / 2;
                int y = (getHeight() + fm.getAscent() - fm.getDescent()) / 2;
                g2.drawString(label, x, y);
                g2.dispose();
            }
        };

        button.setFont(BUTTON);
        button.setForeground(textColor);
        button.setFocusPainted(false);
        button.setOpaque(false);
        button.setContentAreaFilled(false);
        button.setBorder(new EmptyBorder(9, 18, 9, 18));
        button.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        return button;
    }

    public static JLabel label(String text) {
        JLabel label = new JLabel(text);
        label.setFont(LABEL);
        label.setForeground(getText());
        return label;
    }

    public static JLabel heading(String text) {
        JLabel label = new JLabel(text);
        label.setFont(HEADING);
        label.setForeground(getText());
        return label;
    }

    /** Section heading used inside forms (e.g. "Customer Details"). */
    public static JLabel section(String text) {
        JLabel label = new JLabel(text);
        label.setFont(SECTION);
        label.setForeground(getAccent());
        return label;
    }

    public static void styleField(JTextField field) {
        field.setFont(BODY);
        field.setBackground(getCard());
        field.setForeground(getText());
        field.setCaretColor(getText());
        field.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(getLine(), 1, true),
                new EmptyBorder(8, 12, 8, 12)));
    }

    public static void styleCombo(JComboBox<?> combo) {
        combo.setFont(BODY);
        combo.setBackground(getCard());
        combo.setForeground(getText());
    }

    public static void styleTable(JTable table) {
        table.setFont(BODY);
        table.setRowHeight(30);
        table.setBackground(getCard());
        table.setForeground(getText());
        table.setShowVerticalLines(false);
        table.setShowHorizontalLines(true);
        table.setGridColor(getLine());
        table.setIntercellSpacing(new Dimension(0, 1));
        table.setSelectionBackground(getSelection());
        table.setSelectionForeground(getText());
        table.setFillsViewportHeight(true);

        JTableHeader header = table.getTableHeader();
        header.setFont(new Font("Segoe UI", Font.BOLD, 13));
        header.setBackground(darkMode ? DARK_PRIMARY_LIGHT : new Color(248, 250, 252));
        header.setForeground(getText());
        header.setReorderingAllowed(false);
        header.setPreferredSize(new Dimension(header.getWidth(), 36));

        // Center align integer and date/time columns cleanly
        DefaultTableCellRenderer centerRenderer = new DefaultTableCellRenderer();
        centerRenderer.setHorizontalAlignment(SwingConstants.CENTER);
        for (int i = 0; i < table.getColumnCount(); i++) {
            Class<?> colClass = table.getColumnClass(i);
            if (colClass == Integer.class || i == 0 || i == 3 || i == 4 || i == 5 || i == 6) {
                table.getColumnModel().getColumn(i).setCellRenderer(centerRenderer);
            }
        }
    }

    /** Rounded card container with border and internal padding. */
    public static void card(JComponent component) {
        component.setBackground(getCard());
        component.setOpaque(true);
        component.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(getLine(), 1, true),
                new EmptyBorder(16, 20, 16, 20)));
    }

    /** Creates a rounded stat / KPI card for dashboards. */
    public static JPanel statCard(String title, String value, String subtitle, Color accentColor) {
        JPanel card = new JPanel(new BorderLayout(0, 6));
        card.setBackground(getCard());
        card.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createCompoundBorder(
                        BorderFactory.createLineBorder(getLine(), 1, true),
                        BorderFactory.createMatteBorder(0, 4, 0, 0, accentColor)
                ),
                new EmptyBorder(14, 18, 14, 18)
        ));

        JLabel titleLbl = new JLabel(title.toUpperCase());
        titleLbl.setFont(new Font("Segoe UI", Font.BOLD, 11));
        titleLbl.setForeground(getMuted());

        JLabel valLbl = new JLabel(value);
        valLbl.setFont(new Font("Segoe UI", Font.BOLD, 24));
        valLbl.setForeground(getText());

        JLabel subLbl = new JLabel(subtitle);
        subLbl.setFont(SMALL);
        subLbl.setForeground(getMuted());

        JPanel center = new JPanel(new BorderLayout(0, 2));
        center.setOpaque(false);
        center.add(titleLbl, BorderLayout.NORTH);
        center.add(valLbl, BorderLayout.CENTER);
        center.add(subLbl, BorderLayout.SOUTH);

        card.add(center, BorderLayout.CENTER);
        return card;
    }

    /** Creates a small pill badge (e.g. for BOOKED, CANCELLED, ADMIN). */
    public static JLabel badge(String text, Color bg, Color fg) {
        JLabel badge = new JLabel(text, SwingConstants.CENTER) {
            @Override
            protected void paintComponent(Graphics g) {
                Graphics2D g2 = (Graphics2D) g.create();
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                        RenderingHints.VALUE_ANTIALIAS_ON);
                g2.setColor(bg);
                g2.fill(new RoundRectangle2D.Double(0, 0, getWidth() - 1, getHeight() - 1, 12, 12));
                super.paintComponent(g);
                g2.dispose();
            }
        };
        badge.setFont(new Font("Segoe UI", Font.BOLD, 11));
        badge.setForeground(fg);
        badge.setOpaque(false);
        badge.setBorder(new EmptyBorder(3, 8, 3, 8));
        return badge;
    }

    /** Dark banner shown at the top of every dialog. */
    public static JPanel dialogHeader(String title, String subtitle) {
        JPanel header = new JPanel(new BorderLayout());
        header.setBackground(getPrimary());
        header.setBorder(new EmptyBorder(16, 22, 16, 22));

        JLabel titleLabel = new JLabel(title);
        titleLabel.setFont(HEADING);
        titleLabel.setForeground(Color.WHITE);

        JLabel subtitleLabel = new JLabel(subtitle);
        subtitleLabel.setFont(SMALL);
        subtitleLabel.setForeground(new Color(203, 213, 225));

        JPanel text = new JPanel(new BorderLayout(0, 4));
        text.setOpaque(false);
        text.add(titleLabel, BorderLayout.NORTH);
        text.add(subtitleLabel, BorderLayout.SOUTH);

        header.add(text, BorderLayout.CENTER);
        return header;
    }

    // ================================================================
    //  FEEDBACK DIALOGS
    // ================================================================

    public static void info(Component parent, String message) {
        JOptionPane.showMessageDialog(parent, message, "Information",
                JOptionPane.INFORMATION_MESSAGE);
    }

    public static void success(Component parent, String message) {
        JOptionPane.showMessageDialog(parent, message, "Success",
                JOptionPane.INFORMATION_MESSAGE);
    }

    public static void error(Component parent, String message) {
        JOptionPane.showMessageDialog(parent, message, "Error",
                JOptionPane.ERROR_MESSAGE);
    }

    public static boolean confirm(Component parent, String message, String title) {
        return JOptionPane.showConfirmDialog(parent, message, title,
                JOptionPane.YES_NO_OPTION,
                JOptionPane.QUESTION_MESSAGE) == JOptionPane.YES_OPTION;
    }
}

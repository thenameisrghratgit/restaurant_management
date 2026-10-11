package gui;

import dao.ReservationDAO;
import dao.TableDAO;
import model.Customer;
import model.Reservation;
import model.RestaurantTable;
import util.ValidationUtil;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.sql.SQLException;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.format.DateTimeParseException;
import java.util.List;

/**
 * Reservation form: customer details, date/time and an available table.
 * Booking is executed as one database transaction (customer + reservation).
 */
public class ReservationDialog extends JDialog {

    private final JTextField nameField = new JTextField(22);
    private final JTextField phoneField = new JTextField(22);
    private final JTextField emailField = new JTextField(22);
    private final JSpinner guestsSpinner =
            new JSpinner(new SpinnerNumberModel(2, 1, 50, 1));
    private final JTextField dateField = new JTextField(22);
    private final JTextField timeField = new JTextField(22);
    private final JComboBox<RestaurantTable> tableCombo = new JComboBox<>();

    private final TableDAO tableDAO = new TableDAO();
    private final ReservationDAO reservationDAO = new ReservationDAO();

    public ReservationDialog(JFrame owner) {
        super(owner, "Make Reservation", true);
        setSize(660, 660);
        setLocationRelativeTo(owner);
        setMinimumSize(new Dimension(560, 560));
        setLayout(new BorderLayout());

        add(GUITheme.dialogHeader("Make a New Reservation",
                "All fields marked with * are required"), BorderLayout.NORTH);
        add(buildForm(), BorderLayout.CENTER);
        add(buildButtonBar(), BorderLayout.SOUTH);

        resetForm();
        attachChangeListeners();
    }

    public ReservationDialog(JFrame owner, Customer customer) {
        this(owner);
        if (customer != null) {
            if (customer.getName() != null) {
                nameField.setText(customer.getName());
            }
            if (customer.getPhone() != null) {
                phoneField.setText(customer.getPhone());
            }
            if (customer.getEmail() != null) {
                emailField.setText(customer.getEmail());
            }
        }
    }

    // ================================================================
    //  UI CONSTRUCTION
    // ================================================================

    private JScrollPane buildForm() {
        JPanel form = new JPanel(new GridBagLayout());
        GUITheme.card(form);

        GridBagConstraints gc = new GridBagConstraints();
        gc.insets = new Insets(6, 8, 6, 8);
        gc.anchor = GridBagConstraints.WEST;

        int row = 0;

        addSection(form, gc, row++, "Customer Details");
        addRow(form, gc, row++, "Name *", nameField);
        addRow(form, gc, row++, "Phone *", phoneField);
        addRow(form, gc, row++, "Email", emailField);

        addSection(form, gc, row++, "Reservation Details");
        addRow(form, gc, row++, "Number of Guests *", guestsSpinner);
        addRow(form, gc, row++, "Date * (yyyy-MM-dd)", dateField);
        addRow(form, gc, row++, "Time * (HH:mm)", timeField);

        // table row: label + combo + refresh button
        gc.gridx = 0;
        gc.gridy = row;
        gc.gridwidth = 1;
        gc.weightx = 0;
        gc.fill = GridBagConstraints.NONE;
        form.add(GUITheme.label("Available Table *"), gc);

        gc.gridx = 1;
        gc.weightx = 1;
        gc.fill = GridBagConstraints.HORIZONTAL;
        form.add(tableCombo, gc);

        JButton findButton = GUITheme.button("Find Tables",
                GUITheme.PRIMARY_LIGHT);
        findButton.addActionListener(e -> findAvailableTables(true));
        gc.gridx = 2;
        gc.weightx = 0;
        gc.fill = GridBagConstraints.NONE;
        gc.insets = new Insets(6, 4, 6, 8);
        form.add(findButton, gc);

        gc.gridx = 0;
        gc.gridy = row + 1;
        gc.gridwidth = 3;
        gc.insets = new Insets(2, 8, 6, 8);
        JLabel hint = new JLabel(
                "Click 'Find Tables' after entering date, time and guests. "
                        + "Tables already booked for that slot are excluded.");
        hint.setFont(GUITheme.SMALL);
        hint.setForeground(GUITheme.MUTED);
        form.add(hint, gc);

        // filler keeps the form pinned to the top
        GridBagConstraints fillerGc = new GridBagConstraints();
        fillerGc.gridx = 0;
        fillerGc.gridy = row + 2;
        fillerGc.gridwidth = 3;
        fillerGc.weighty = 1;
        fillerGc.fill = GridBagConstraints.VERTICAL;
        form.add(Box.createVerticalGlue(), fillerGc);

        JScrollPane scroll = new JScrollPane(form);
        scroll.setBorder(null);
        scroll.getViewport().setBackground(GUITheme.CARD);
        return scroll;
    }

    private JPanel buildButtonBar() {
        JPanel bar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 14));
        bar.setBackground(GUITheme.BACKGROUND);

        JButton bookButton = GUITheme.button("Book Reservation",
                GUITheme.ACCENT);
        bookButton.addActionListener(e -> bookReservation());

        JButton clearButton = GUITheme.button("Clear Form",
                GUITheme.PRIMARY_LIGHT);
        clearButton.addActionListener(e -> resetForm());

        JButton closeButton = GUITheme.button("Close", GUITheme.PRIMARY);
        closeButton.addActionListener(e -> dispose());

        bar.add(clearButton);
        bar.add(closeButton);
        bar.add(bookButton);
        return bar;
    }

    private void addSection(JPanel panel, GridBagConstraints gc,
                            int row, String text) {

        gc.gridx = 0;
        gc.gridy = row;
        gc.gridwidth = 3;
        gc.weightx = 1;
        gc.fill = GridBagConstraints.HORIZONTAL;
        gc.insets = new Insets(14, 8, 6, 8);
        panel.add(GUITheme.section(text), gc);

        gc.insets = new Insets(6, 8, 6, 8);
    }

    private void addRow(JPanel panel, GridBagConstraints gc,
                        int row, String labelText, JComponent field) {

        gc.gridx = 0;
        gc.gridy = row;
        gc.gridwidth = 1;
        gc.weightx = 0;
        gc.fill = GridBagConstraints.NONE;
        panel.add(GUITheme.label(labelText), gc);

        gc.gridx = 1;
        gc.gridwidth = 2;
        gc.weightx = 1;
        gc.fill = GridBagConstraints.HORIZONTAL;
        panel.add(field, gc);
    }

    // ================================================================
    //  EVENTS
    // ================================================================

    /** Any change to date/time/guests invalidates the current table list. */
    private void attachChangeListeners() {
        guestsSpinner.addChangeListener(e -> clearTableList());

        javax.swing.event.DocumentListener invalidateTables =
                new javax.swing.event.DocumentListener() {
                    @Override
                    public void insertUpdate(
                            javax.swing.event.DocumentEvent e) {
                        clearTableList();
                    }

                    @Override
                    public void removeUpdate(
                            javax.swing.event.DocumentEvent e) {
                        clearTableList();
                    }

                    @Override
                    public void changedUpdate(
                            javax.swing.event.DocumentEvent e) {
                        clearTableList();
                    }
                };

        dateField.getDocument().addDocumentListener(invalidateTables);
        timeField.getDocument().addDocumentListener(invalidateTables);
    }

    private void clearTableList() {
        tableCombo.removeAllItems();
    }

    // ================================================================
    //  LOGIC
    // ================================================================

    private void resetForm() {
        nameField.setText("");
        phoneField.setText("");
        emailField.setText("");
        guestsSpinner.setValue(2);
        dateField.setText(LocalDate.now().toString());
        timeField.setText("19:00");
        clearTableList();
    }

    /** Clears only the customer section (used after a successful booking). */
    private void clearCustomerFields() {
        nameField.setText("");
        phoneField.setText("");
        emailField.setText("");
    }

    /** Loads the table list for the entered date, time and guest count. */
    private void findAvailableTables(boolean showFeedback) {
        LocalDate date;
        LocalTime time;
        int guests;

        try {
            date = ValidationUtil.parseDate(dateField.getText());
            time = ValidationUtil.parseTime(timeField.getText());
        } catch (DateTimeParseException e) {
            GUITheme.error(this,
                    "Please enter a valid date (yyyy-MM-dd) and time (HH:mm) "
                            + "before searching for tables.");
            return;
        }

        guests = (Integer) guestsSpinner.getValue();

        try {
            List<RestaurantTable> available =
                    tableDAO.getAvailableTables(date, time, guests, -1);

            tableCombo.removeAllItems();
            for (RestaurantTable table : available) {
                tableCombo.addItem(table);
            }

            if (available.isEmpty()) {
                if (showFeedback) {
                    GUITheme.info(this,
                            "No table with " + guests + " or more seats is "
                                    + "free on " + date + " at "
                                    + String.format("%02d:%02d",
                                    time.getHour(), time.getMinute()) + ".");
                }
            } else if (showFeedback) {
                GUITheme.info(this, available.size()
                        + " table(s) available for the requested slot.");
            }

        } catch (SQLException e) {
            handleSqlError(e);
        }
    }

    /** Validates the whole form and books the reservation. */
    private void bookReservation() {

        // ----- 1. validation -----
        String name = nameField.getText().trim();
        String phone = phoneField.getText().trim();
        String email = emailField.getText().trim();

        if (ValidationUtil.isBlank(name)) {
            GUITheme.error(this, "Customer name is required.");
            nameField.requestFocus();
            return;
        }
        if (name.length() > 100) {
            GUITheme.error(this, "Customer name must be 100 characters or fewer.");
            return;
        }
        if (!ValidationUtil.isValidPhone(phone)) {
            GUITheme.error(this,
                    "Enter a valid phone number (10-15 digits, optional '+').");
            phoneField.requestFocus();
            return;
        }
        if (!ValidationUtil.isBlank(email)
                && !ValidationUtil.isValidEmail(email)) {
            GUITheme.error(this, "Enter a valid email address "
                    + "(e.g. name@example.com) or leave it empty.");
            emailField.requestFocus();
            return;
        }

        int guests = (Integer) guestsSpinner.getValue();
        if (guests <= 0) {
            GUITheme.error(this, "Number of guests must be at least 1.");
            return;
        }

        LocalDate date;
        LocalTime time;
        try {
            date = ValidationUtil.parseDate(dateField.getText());
            time = ValidationUtil.parseTime(timeField.getText());
        } catch (DateTimeParseException e) {
            GUITheme.error(this,
                    "Invalid date or time.\nUse date: yyyy-MM-dd "
                            + "and time: HH:mm (e.g. 2026-10-10 / 19:30).");
            return;
        }

        if (ValidationUtil.isPastSlot(date, time)) {
            GUITheme.error(this,
                    "The reservation date and time cannot be in the past.");
            return;
        }

        RestaurantTable table =
                (RestaurantTable) tableCombo.getSelectedItem();
        if (table == null) {
            GUITheme.error(this,
                    "No table selected.\nClick 'Find Tables' and choose an "
                            + "available table.");
            return;
        }

        if (!ValidationUtil.isValidGuestCount(guests, table.getCapacity())) {
            GUITheme.error(this,
                    "Table " + table.getTableNumber() + " seats "
                            + table.getCapacity() + " guests, but you entered "
                            + guests + ".\nPlease reduce the guests or pick a "
                            + "larger table.");
            return;
        }

        // ----- 2. re-check availability directly in the database -----
        try {
            if (!reservationDAO.isTableSlotFree(table.getTableId(),
                    date, time, -1)) {
                GUITheme.error(this,
                        "Table " + table.getTableNumber() + " was just booked "
                                + "for that date and time.\n"
                                + "Please run 'Find Tables' again.");
                findAvailableTables(false);
                return;
            }

            // ----- 3. insert customer + reservation in one transaction -----
            Customer customer = new Customer(name, phone,
                    ValidationUtil.isBlank(email) ? null : email);

            Reservation reservation = new Reservation(
                    0, table.getTableId(), date, time, guests);

            int reservationId =
                    reservationDAO.bookReservation(customer, reservation);

            GUITheme.success(this,
                    "Reservation #" + reservationId + " booked successfully!\n\n"
                            + "Customer: " + name + "\n"
                            + "Table: " + table.getTableNumber() + "\n"
                            + "Guests: " + guests + "\n"
                            + "When: " + date + " at "
                            + String.format("%02d:%02d",
                            time.getHour(), time.getMinute()));

            // clear the customer details and refresh the table list so the
            // remaining free tables for this slot are shown immediately
            clearCustomerFields();
            findAvailableTables(false);
            nameField.requestFocus();

        } catch (SQLException e) {
            handleSqlError(e);
        }
    }

    private void handleSqlError(SQLException e) {
        e.printStackTrace();
        GUITheme.error(this,
                "A database error occurred:\n" + e.getMessage());
    }
}

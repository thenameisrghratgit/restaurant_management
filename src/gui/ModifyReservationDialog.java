package gui;

import dao.ReservationDAO;
import dao.TableDAO;
import model.Reservation;
import model.ReservationDetail;
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
 * Select an existing reservation and update its table, date, time,
 * guest count or status (UPDATE statement).
 */
public class ModifyReservationDialog extends JDialog {

    private final ReservationListPanel listPanel = new ReservationListPanel();
    private final JLabel selectedLabel =
            GUITheme.label("Select a reservation in the list above.");

    private final JTextField dateField = new JTextField(18);
    private final JTextField timeField = new JTextField(18);
    private final JSpinner guestsSpinner =
            new JSpinner(new SpinnerNumberModel(2, 1, 50, 1));
    private final JComboBox<RestaurantTable> tableCombo = new JComboBox<>();
    private final JComboBox<String> statusCombo =
            new JComboBox<>(new String[]{"BOOKED", "COMPLETED", "CANCELLED"});

    private final ReservationDAO reservationDAO = new ReservationDAO();
    private final TableDAO tableDAO = new TableDAO();

    private ReservationDetail current;
    private boolean updating;

    public ModifyReservationDialog(JFrame owner) {
        super(owner, "Modify Reservation", true);
        setSize(960, 700);
        setLocationRelativeTo(owner);
        setMinimumSize(new Dimension(800, 600));
        setLayout(new BorderLayout());

        add(GUITheme.dialogHeader("Modify Reservation",
                "Select a reservation, change its details and save (UPDATE)"),
                BorderLayout.NORTH);
        add(buildSplitPane(), BorderLayout.CENTER);
        add(buildButtonBar(), BorderLayout.SOUTH);

        attachListeners();
        loadReservations();
    }

    // ================================================================
    //  UI CONSTRUCTION
    // ================================================================

    private JSplitPane buildSplitPane() {
        JPanel top = new JPanel(new BorderLayout(0, 8));
        top.setBackground(GUITheme.BACKGROUND);
        top.setBorder(new EmptyBorder(12, 16, 8, 16));

        JPanel toolbar = new JPanel(new BorderLayout());
        toolbar.setOpaque(false);

        JButton refresh = GUITheme.button("Refresh List",
                GUITheme.PRIMARY_LIGHT);
        refresh.addActionListener(e -> loadReservations());
        toolbar.add(refresh, BorderLayout.WEST);

        JLabel hint = new JLabel(
                "Click a row to load it into the form below");
        hint.setFont(GUITheme.SMALL);
        hint.setForeground(GUITheme.MUTED);
        toolbar.add(hint, BorderLayout.EAST);

        top.add(toolbar, BorderLayout.NORTH);
        top.add(listPanel, BorderLayout.CENTER);

        JPanel bottom = new JPanel(new BorderLayout());
        bottom.setBackground(GUITheme.BACKGROUND);
        bottom.setBorder(new EmptyBorder(8, 16, 8, 16));
        bottom.add(buildForm(), BorderLayout.CENTER);
        bottom.add(selectedLabel, BorderLayout.NORTH);

        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, top, bottom);
        split.setResizeWeight(0.45);
        split.setBorder(null);
        return split;
    }

    private JPanel buildForm() {
        JPanel form = new JPanel(new GridBagLayout());
        GUITheme.card(form);

        GridBagConstraints gc = new GridBagConstraints();
        gc.insets = new Insets(6, 8, 6, 8);
        gc.anchor = GridBagConstraints.WEST;

        int row = 0;
        row = addRow(form, gc, row, "Date * (yyyy-MM-dd)", dateField);
        row = addRow(form, gc, row, "Time * (HH:mm)", timeField);
        row = addRow(form, gc, row, "Number of Guests *", guestsSpinner);

        // table row with a refresh button
        gc.gridx = 0;
        gc.gridy = row;
        gc.weightx = 0;
        gc.fill = GridBagConstraints.NONE;
        form.add(GUITheme.label("Table *"), gc);

        gc.gridx = 1;
        gc.weightx = 1;
        gc.fill = GridBagConstraints.HORIZONTAL;
        form.add(tableCombo, gc);

        JButton refreshTables = GUITheme.button("Refresh Tables",
                GUITheme.PRIMARY_LIGHT);
        refreshTables.addActionListener(e -> refreshTableCombo(true));
        gc.gridx = 2;
        gc.weightx = 0;
        gc.fill = GridBagConstraints.NONE;
        gc.insets = new Insets(6, 4, 6, 8);
        form.add(refreshTables, gc);

        gc.insets = new Insets(6, 8, 6, 8);
        row++;

        row = addRow(form, gc, row, "Status", statusCombo);

        GridBagConstraints filler = new GridBagConstraints();
        filler.gridx = 0;
        filler.gridy = row;
        filler.gridwidth = 3;
        filler.weighty = 1;
        filler.fill = GridBagConstraints.VERTICAL;
        form.add(Box.createVerticalGlue(), filler);

        return form;
    }

    private int addRow(JPanel panel, GridBagConstraints gc, int row,
                       String labelText, JComponent field) {

        gc.gridx = 0;
        gc.gridy = row;
        gc.gridwidth = 1;
        gc.weightx = 0;
        gc.fill = GridBagConstraints.NONE;
        gc.insets = new Insets(6, 8, 6, 8);
        panel.add(GUITheme.label(labelText), gc);

        gc.gridx = 1;
        gc.gridwidth = 2;
        gc.weightx = 1;
        gc.fill = GridBagConstraints.HORIZONTAL;
        panel.add(field, gc);

        return row + 1;
    }

    private JPanel buildButtonBar() {
        JPanel bar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 12));
        bar.setBackground(GUITheme.BACKGROUND);

        JButton save = GUITheme.button("Save Changes", GUITheme.ACCENT);
        save.addActionListener(e -> saveChanges());

        JButton clear = GUITheme.button("Clear Selection",
                GUITheme.PRIMARY_LIGHT);
        clear.addActionListener(e -> clearSelection());

        JButton close = GUITheme.button("Close", GUITheme.PRIMARY);
        close.addActionListener(e -> dispose());

        bar.add(clear);
        bar.add(close);
        bar.add(save);
        return bar;
    }

    // ================================================================
    //  EVENTS
    // ================================================================

    private void attachListeners() {
        // load the selected reservation into the form
        listPanel.getTable().getSelectionModel().addListSelectionListener(e -> {
            if (!e.getValueIsAdjusting() && !updating) {
                loadSelectedReservation();
            }
        });

        // re-query the table list when the user leaves date/time/guests
        java.awt.event.FocusAdapter refreshOnExit =
                new java.awt.event.FocusAdapter() {
                    @Override
                    public void focusLost(java.awt.event.FocusEvent e) {
                        if (current != null) {
                            refreshTableCombo(false);
                        }
                    }
                };

        dateField.addFocusListener(refreshOnExit);
        timeField.addFocusListener(refreshOnExit);
        guestsSpinner.addFocusListener(refreshOnExit);
    }

    // ================================================================
    //  LOGIC
    // ================================================================

    private void loadReservations() {
        try {
            clearSelection();
            listPanel.setReservations(
                    reservationDAO.getAllReservationDetails());
        } catch (SQLException e) {
            e.printStackTrace();
            GUITheme.error(this,
                    "Could not load reservations:\n" + e.getMessage());
        }
    }

    private void loadSelectedReservation() {
        ReservationDetail selected = listPanel.getSelectedReservation();
        if (selected == null) {
            return;
        }

        current = selected;
        updating = true;
        try {
            selectedLabel.setText("Editing reservation #"
                    + current.getReservationId() + " - "
                    + current.getCustomerName() + " ("
                    + current.getPhone() + ")");

            dateField.setText(current.getDateText());
            timeField.setText(current.getTimeText());
            guestsSpinner.setValue(Math.max(1, current.getGuests()));
            statusCombo.setSelectedItem(
                    current.getStatus() == null ? "BOOKED" : current.getStatus());

            refreshTableCombo(false);
        } finally {
            updating = false;
        }
    }

    /** Rebuilds the table list for the values currently in the form. */
    private void refreshTableCombo(boolean showFeedback) {
        if (current == null) {
            return;
        }

        LocalDate date;
        LocalTime time;
        int guests = (Integer) guestsSpinner.getValue();

        try {
            date = ValidationUtil.parseDate(dateField.getText());
            time = ValidationUtil.parseTime(timeField.getText());
        } catch (DateTimeParseException e) {
            if (showFeedback) {
                GUITheme.error(this,
                        "Enter a valid date (yyyy-MM-dd) and time (HH:mm) "
                                + "first.");
            }
            return;
        }

        try {
            // exclude this reservation so its own table still shows up
            List<RestaurantTable> tables =
                    tableDAO.getAvailableTables(date, time,
                            Math.max(1, guests),
                            current.getReservationId());

            tableCombo.removeAllItems();
            RestaurantTable currentTable = null;

            for (RestaurantTable table : tables) {
                tableCombo.addItem(table);
                if (table.getTableId() == current.getTableId()) {
                    currentTable = table;
                }
            }

            if (currentTable != null) {
                tableCombo.setSelectedItem(currentTable);
            }

            if (showFeedback) {
                GUITheme.info(this, tables.size()
                        + " table(s) can be used for that slot.");
            }

        } catch (SQLException e) {
            e.printStackTrace();
            GUITheme.error(this,
                    "Could not load tables:\n" + e.getMessage());
        }
    }

    private void saveChanges() {
        if (current == null) {
            GUITheme.error(this,
                    "Select a reservation from the list first.");
            return;
        }

        // ----- validation -----
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
                    "No table selected.\nUse 'Refresh Tables' and pick a "
                            + "table for the new slot.");
            return;
        }

        int guests = (Integer) guestsSpinner.getValue();
        if (guests <= 0) {
            GUITheme.error(this, "Number of guests must be at least 1.");
            return;
        }
        if (guests > table.getCapacity()) {
            GUITheme.error(this,
                    "Table " + table.getTableNumber() + " seats "
                            + table.getCapacity() + " guests, but you entered "
                            + guests + ".");
            return;
        }

        String status = (String) statusCombo.getSelectedItem();

        // ----- conflict check (ignore this reservation's own booking) -----
        try {
            if (!"CANCELLED".equals(status)
                    && !reservationDAO.isTableSlotFree(table.getTableId(),
                    date, time, current.getReservationId())) {

                GUITheme.error(this,
                        "Table " + table.getTableNumber()
                                + " is already booked for " + date + " at "
                                + String.format("%02d:%02d",
                                time.getHour(), time.getMinute())
                                + ".\nChoose another table, date or time.");
                refreshTableCombo(false);
                return;
            }

            // ----- UPDATE -----
            Reservation reservation = new Reservation(
                    current.getReservationId(),
                    current.getCustomerId(),
                    table.getTableId(),
                    date,
                    time,
                    guests,
                    status);

            boolean updated = reservationDAO.updateReservation(reservation);

            if (updated) {
                int id = current.getReservationId();
                GUITheme.success(this,
                        "Reservation #" + id + " updated successfully.\n\n"
                                + "Table: " + table.getTableNumber() + "\n"
                                + "Guests: " + guests + "\n"
                                + "When: " + date + " at "
                                + String.format("%02d:%02d",
                                time.getHour(), time.getMinute())
                                + "\nStatus: " + status);

                loadReservations();
                listPanel.selectById(id);
            } else {
                GUITheme.error(this,
                        "The reservation could not be updated "
                                + "(it may have been deleted).");
                loadReservations();
            }

        } catch (SQLException e) {
            e.printStackTrace();
            GUITheme.error(this,
                    "Database error while updating:\n" + e.getMessage());
        }
    }

    private void clearSelection() {
        listPanel.clearSelection();
        current = null;
        selectedLabel.setText("Select a reservation in the list above.");
        tableCombo.removeAllItems();
        dateField.setText("");
        timeField.setText("");
        statusCombo.setSelectedItem("BOOKED");
    }
}

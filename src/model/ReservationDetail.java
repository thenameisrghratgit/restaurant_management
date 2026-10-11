package model;

import java.time.LocalDate;
import java.time.LocalTime;

/**
 * Read-only projection of a reservation joined with its customer and table.
 * Used whenever the GUI needs display-friendly data (names and table numbers
 * instead of raw foreign-key IDs).
 */
public class ReservationDetail {

    private int reservationId;
    private int customerId;
    private int tableId;
    private int tableNumber;
    private String customerName;
    private String phone;
    private LocalDate reservationDate;
    private LocalTime reservationTime;
    private int guests;
    private String status;

    public ReservationDetail() {
    }

    public ReservationDetail(int reservationId, int customerId, int tableId,
                             int tableNumber, String customerName, String phone,
                             LocalDate reservationDate, LocalTime reservationTime,
                             int guests, String status) {

        this.reservationId = reservationId;
        this.customerId = customerId;
        this.tableId = tableId;
        this.tableNumber = tableNumber;
        this.customerName = customerName;
        this.phone = phone;
        this.reservationDate = reservationDate;
        this.reservationTime = reservationTime;
        this.guests = guests;
        this.status = status;
    }

    // ----- convenience display helpers -----

    public String getDateText() {
        return reservationDate == null ? "" : reservationDate.toString();
    }

    public String getTimeText() {
        if (reservationTime == null) {
            return "";
        }
        return String.format("%02d:%02d",
                reservationTime.getHour(), reservationTime.getMinute());
    }

    // ----- getters and setters -----

    public int getReservationId() {
        return reservationId;
    }

    public void setReservationId(int reservationId) {
        this.reservationId = reservationId;
    }

    public int getCustomerId() {
        return customerId;
    }

    public void setCustomerId(int customerId) {
        this.customerId = customerId;
    }

    public int getTableId() {
        return tableId;
    }

    public void setTableId(int tableId) {
        this.tableId = tableId;
    }

    public int getTableNumber() {
        return tableNumber;
    }

    public void setTableNumber(int tableNumber) {
        this.tableNumber = tableNumber;
    }

    public String getCustomerName() {
        return customerName;
    }

    public void setCustomerName(String customerName) {
        this.customerName = customerName;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public LocalDate getReservationDate() {
        return reservationDate;
    }

    public void setReservationDate(LocalDate reservationDate) {
        this.reservationDate = reservationDate;
    }

    public LocalTime getReservationTime() {
        return reservationTime;
    }

    public void setReservationTime(LocalTime reservationTime) {
        this.reservationTime = reservationTime;
    }

    public int getGuests() {
        return guests;
    }

    public void setGuests(int guests) {
        this.guests = guests;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}

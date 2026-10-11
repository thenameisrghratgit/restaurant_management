package model;

import java.time.LocalDate;
import java.time.LocalTime;

public class Reservation {

    private int reservationId;
    private int customerId;
    private int tableId;
    private LocalDate reservationDate;
    private LocalTime reservationTime;
    private int guests;
    private String status;

    public Reservation() {
    }

    public Reservation(int reservationId, int customerId, int tableId,
                       LocalDate reservationDate,
                       LocalTime reservationTime,
                       int guests, String status) {

        this.reservationId = reservationId;
        this.customerId = customerId;
        this.tableId = tableId;
        this.reservationDate = reservationDate;
        this.reservationTime = reservationTime;
        this.guests = guests;
        this.status = status;
    }

    public Reservation(int customerId, int tableId,
                       LocalDate reservationDate,
                       LocalTime reservationTime,
                       int guests) {

        this.customerId = customerId;
        this.tableId = tableId;
        this.reservationDate = reservationDate;
        this.reservationTime = reservationTime;
        this.guests = guests;
        this.status = "BOOKED";
    }

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
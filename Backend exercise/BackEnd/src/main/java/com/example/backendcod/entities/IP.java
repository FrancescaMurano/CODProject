package com.example.backendcod.entities;

import java.sql.Timestamp;

public class IP {
    private String IP_number;
    private Long timeinmillis;
    private Integer attempts;

    public IP(String IP_number, Long time, Integer attempts){
        this.IP_number = IP_number;
        this.timeinmillis = time;
        this.attempts = attempts;
    }
    public IP(String IP_number){
        this.IP_number = IP_number;
        this.timeinmillis = new Timestamp(System.currentTimeMillis()).getTime();
        this.attempts = 1;
    }

    public void setIP_number(String iP_number) {
        IP_number = iP_number;
    }

    public void setTimeinMillis(Long timeinmillis) {
        this.timeinmillis = timeinmillis;
    }

    public void setAttempts(Integer attempts) {
        this.attempts = attempts;
    }

    public String getIP_number() {
        return IP_number;
    }

    public Long getTimeinmillis() {
        return timeinmillis;
    }

    public Integer getAttempts() {
        return attempts;
    }

    public String toString(){
        return IP_number + ", " + timeinmillis + ", " + attempts;
    }
}

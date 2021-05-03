import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({providedIn: 'root'})
export class LandingService {
    
    private userURL = "http://localhost:8080/api/users/?page_size=902&page_number=0";
    private recommendationURL = "http://localhost:8080/api/recommendation/?uuid=b12408f0-d239-49cb-8098-c88f76fad069&research_interest=Information retrieval&sim_weight=0.3&page_size=2&page_number=0";

    constructor(private http: HttpClient) {}

    getAllUsers() {
        try {
            return this.http.get(this.userURL);
        } catch(err) {
            console.log(err);
        }
    }

    getInformation() {
        try {
            return this.http.get(this.recommendationURL);
        } catch(err) {
            console.log(err);
        }
    }
}
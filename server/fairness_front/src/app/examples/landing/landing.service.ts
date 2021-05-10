import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({providedIn: 'root'})
export class LandingService {
    
    private BASE_URL: string = "http://localhost:8080/api/";
    
    constructor(private http: HttpClient) {}

    getAllUsers(page_number, page_size) {

        const userURL: string = this.BASE_URL + `users/?page_size=${ page_size }&page_number=${ page_number }`;

        try {
            return this.http.get(userURL);
        } catch(err) {
            console.log(err);
        }
    }

    getResearchInterestList() {

        const researchInterestURL:string = this.BASE_URL + "researchInterests/";

        try {
            return this.http.get(researchInterestURL);
        } catch(err) {
            console.log(err);
        }
    }
    
    getRecommendation(uuid, research_interest, sim_weight, page_number, page_size) {

        const path: string = `recommendation/?uuid=${ uuid }&research_interest=${ research_interest }&sim_weight=${ sim_weight }&page_size=${ page_size }&page_number=${ page_number }`;
        const recommendationURL: string = this.BASE_URL + path;

        try {
            return this.http.get(recommendationURL);
        } catch(err) {
            console.log(err);
        }
    }
}
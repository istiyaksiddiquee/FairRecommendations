import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({ providedIn: "root" })
export class LandingService {
  private BASE_URL: string = "http://localhost:8080/api/";

  constructor(private http: HttpClient) {}

  getAllUsers(page_number, page_size, header_for_backend) {
    const userURL: string =
      this.BASE_URL +
      `users/?page_size=${page_size}&page_number=${page_number}`;
    const token = "JWT " + header_for_backend;

    const headers: HttpHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: token,
    });

    try {
      return this.http.get(userURL, 
        {
            headers: headers
        });
    } catch (err) {
      console.log(err);
    }
  }

  getResearchInterestList(header_for_backend) {
    const researchInterestURL: string = this.BASE_URL + "researchInterests/";
    const token = "JWT " + header_for_backend;

    const headers: HttpHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: token,
    });

    try {
      return this.http.get(researchInterestURL, 
        {
            headers: headers
        });
    } catch (err) {
      console.log(err);
    }
  }

  getRecommendation(
    uuid,
    research_interest,
    sim_weight,
    page_number,
    page_size,
    header_for_backend
  ) {
    const path: string = `recommendation/?uuid=${uuid}&research_interest=${research_interest}&sim_weight=${sim_weight}&page_size=${page_size}&page_number=${page_number}`;
    const recommendationURL: string = this.BASE_URL + path;

    const token = "JWT " + header_for_backend;

    const headers: HttpHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: token,
    });

    try {
      return this.http.get(recommendationURL, {
        headers: headers,
      });
    } catch (err) {
      console.log(err);
    }
  }

  performInitialCheckup(header_for_backend) {
    const path: string = `initialization/`;
    const initializationURL: string = this.BASE_URL + path;
    const token = "JWT " + header_for_backend;

    const headers: HttpHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: token,
    });

    return this.http.get(initializationURL, {
      headers: headers,
    });
  }
}

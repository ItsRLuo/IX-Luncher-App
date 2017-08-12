import { Injectable } from '@angular/core'
import { Http , Response, Headers, RequestOptions } from '@angular/http'

import 'rxjs';
import { Observable } from 'rxjs/Observable'

@Injectable()
export class IXLuncApi {
    private baseUrl = 'https://ix-luncher-api.appspot.com/menu'
    private postRating = 'https://ix-luncher-api.appspot.com/rating/'
    private baseUrl1 = 'data/nextDayMenu.json'
    private topratedUrl1 = 'data/top.json'
    private commentsUrl = 'http://localhost:3000/api/comments';
    private topratedUrl = 'https://ix-luncher-api.appspot.com/food/?tops=10'
    private nextDay =  'data/nextDayMenu.json'
    private previousDay = 'data/previousDayMenu.json'
    private today = 'data/menu.json'

    constructor(public http: Http) { }

    getLunchMenu(city: string, date: any){
        city = "Toronto";
        if(city === "Toronto" || city === "Mississauga" || city === "Brampton") {
            city = "_Wingold"
        }

        if(city === "Kitchner") {
            city = "_KW"
        }

        if(city === "Montreal") {
            city = "_MON"
        }
        let parameters = "/?menuID="+date+city; 
        return new Promise(resolve => {
            this.http.get(`${this.baseUrl}${parameters}`)
                .subscribe(res => resolve(res.json()))
        });
    }

    getLunchMenuNextDay(city: string, date: any){
        let parameters = "?location=" + city + "&date="+date; 
        return new Promise(resolve => {
            this.http.get(`${this.nextDay}`)
                .subscribe(res => resolve(res.json()))
        });
    }

    getLunchMenuPreviousDay(city: string, date: any){
        let parameters = "?location=" + city + "&date="+date; 
        return new Promise(resolve => {
            this.http.get(`${this.previousDay}`)
                .subscribe(res => resolve(res.json()))
        });
    }

    getTopRated(){
        return new Promise(resolve => {
            this.http.get(`${this.topratedUrl1}`)
                .subscribe(res => resolve(res.json()))
        });
    }

    addRating(body: Object): Promise<any> {
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });


    
    console.log(JSON.stringify(body));
    return this.http.post(this.postRating, body, options).toPromise()
           .then(this.extractData) 
           .catch(this.handleErrorPromise); 
    } 

     addRating1 (body: Object): Observable<any> {
         return null;
        /*let bodyString = JSON.stringify(body); // Stringify payload
        let headers      = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options       = new RequestOptions({ headers: headers }); // Create a request option
        console.log("The post for rating! " + JSON.stringify(body))
        return this.http.put(this.baseUrl1, body, options) // ...using post request
                         .map((res:Response) => res.json()) // ...and calling .json() on the response to return data
                         .catch((error:any) => Observable.throw(error.json().error || 'Server error')); //...errors if any
    */} 

    private extractData(res: Response) {
        console.log()
	    let body = res.json();
         console.log(JSON.stringify(body))
        return body.data || {};
    }

    private handleErrorPromise (error: Response | any) {
	    console.error(error.message || error);
	    return Promise.reject(error.message || error);
    }	
}
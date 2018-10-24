extern crate tiny_http;
extern crate reqwest;

use tiny_http::{Server, Response};
use std::net::SocketAddr;

const PORT: u16 = 8118;
const IPME: &str = "https://icanhazip.com";

fn get_ip() -> reqwest::Result<String> {
    match reqwest::get(IPME) {
        Ok(mut r) => {
            if r.status().is_success() {
                r.text()
            } else {
                Ok(format!("Error: {:?}", r))
            }
        },
        Err(e) => Err(e),
    }
}

fn main() {

    let addr = SocketAddr::from(([0,0,0,0], PORT));
    let server = Server::http(addr).expect("protect and serve");

    for req in server.incoming_requests() {
        println!("{:?}", req);
        let ip: String = get_ip().unwrap_or_else(|e| e.to_string());
        let rsp = Response::from_string(ip);
        if let Err(e) = req.respond(rsp) {
            eprintln!("Response failed ({}), continuing...", e);
        }
    }
}

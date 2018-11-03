package ucvproject.uni.victoralin10.com.ucv_app.util;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class Requests {

    public static String request(String url_endpoint, String method, String data) {
        URL url;
        StringBuilder response = new StringBuilder();
        try {
            url = new URL(url_endpoint);
        } catch (MalformedURLException e) {
            throw new IllegalArgumentException("invalid url");
        }

        HttpURLConnection conn = null;
        try {
            conn = (HttpURLConnection) url.openConnection();
            conn.setDoOutput(data != null);
            conn.setDoInput(true);
            conn.setUseCaches(false);
            conn.setRequestMethod(method);
            conn.setRequestProperty("Content-Type", "application/json;charset=UTF-8");

            // Sending
            if (data != null) {
                BufferedWriter out = new BufferedWriter(new OutputStreamWriter(conn.getOutputStream()));
                out.write(data, 0, data.length());
                out.close();
            }

            // Downloading
            BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (conn != null) {
                conn.disconnect();
            }
        }

        return response.toString();
    }

    public static String get(String url) {
        return request(url, "GET", null);
    }

    public static String post(String url, String data) {
        return request(url, "POST", data);
    }
}

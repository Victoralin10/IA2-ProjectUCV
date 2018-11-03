package ucvproject.uni.victoralin10.com.ucv_app.util;

import org.json.JSONException;
import org.json.JSONObject;

public class JSONParser {

    public static JSONObject getJSONFromUrl(String url, String method, String data) {
        JSONObject ans = null;
        String response = Requests.request(url, method, data);

        try {
            ans = new JSONObject(response);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        return ans;
    }
}
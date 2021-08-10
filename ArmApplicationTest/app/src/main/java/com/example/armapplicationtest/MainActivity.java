package com.example.armapplicationtest;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {

    private RequestQueue requestQueue;
    private static String rotateURL = "http://192.168.0.138:5000/rotate";
    private static String getCurrDegreeURL = "http://192.168.0.138:5000/current_degree";
    private static int currDegree;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        requestQueue = Volley.newRequestQueue(this);
        currDegree = 0;
        try {
            requestQueue.add(rotateBtnHelper());
        } catch(Exception e) {
            System.out.println(e);
        }
    }

    // rotate button 0 method by -18 degree increments
    public void onRotateBtn0Click(View view) {
        if (currDegree > 0) {
            currDegree -= 18;
            try {
                requestQueue.add(rotateBtnHelper());

            } catch (Exception e) {
                System.out.println(e);
            }
        }
    }

    // rotate button 180 method by 18 degree increments
    public void onRotateBtn180Click(View view) {
        if (currDegree < 180) {
            currDegree += 18;
            try {
                requestQueue.add(rotateBtnHelper());
            } catch (Exception e) {
                System.out.println(e);
            }
        }
    }

    // rotate helper method
    public static JsonObjectRequest rotateBtnHelper() throws Exception {
            JSONObject jsonDegreeObject = new JSONObject().put("degree", Integer.valueOf(currDegree));
            JsonObjectRequest objectRequest = new JsonObjectRequest(
                    Request.Method.POST,
                    rotateURL,
                    jsonDegreeObject,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            Log.e("Rest Response", response.toString());
                        }
                    },
                    new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            Log.e("Rest Response", error.toString());
                        }
                    }
            );
            return objectRequest;
    }

}
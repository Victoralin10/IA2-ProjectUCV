package ucvproject.uni.victoralin10.com.ucv_app.view;

import android.app.ProgressDialog;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.util.Base64OutputStream;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

import ucvproject.uni.victoralin10.com.ucv_app.util.JSONParser;
import ucvproject.uni.victoralin10.com.ucv_app.R;


public class Register extends AppCompatActivity {
    private EditText user, pass;
    private Button mRegister;
    private MediaRecorder grabacion;
    private String archivoSalida = null;
    private Button btn_recorder;
    // Progress Dialog
    private ProgressDialog pDialog;

    //si lo trabajan de manera local en xxx.xxx.x.x va su ip local
    // private static final String REGISTER_URL = "http://xxx.xxx.x.x:1234/cas/register.php";

    //testing on Emulator:
    private static final String REGISTER_URL = "https://0n31isnqy6.execute-api.us-east-1.amazonaws.com/prod/register";

    //ids
    private static final String TAG_SUCCESS = "success";
    private static final String TAG_MESSAGE = "message";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // TODO Auto-generated method stub
        super.onCreate(savedInstanceState);
        setContentView(R.layout.register);

        user = (EditText) findViewById(R.id.username);
        pass = (EditText) findViewById(R.id.password);

        mRegister = (Button) findViewById(R.id.register);
        //mRegister.setOnClickListener(this);
        btn_recorder = (Button) findViewById(R.id.btn_rec);
        archivoSalida = null;
    }

    public void registrar(View v) {
        // TODO Auto-generated method stub
        if (archivoSalida == null) {
            Toast.makeText(getApplicationContext(), "Aún no graba un audio.", Toast.LENGTH_SHORT).show();
            return;
        }

        new CreateUser().execute();
    }

    class CreateUser extends AsyncTask<String, String, String> {

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            pDialog = new ProgressDialog(Register.this);
            pDialog.setMessage("Creating User...");
            pDialog.setIndeterminate(false);
            pDialog.setCancelable(true);
            pDialog.show();
        }

        @Override
        protected String doInBackground(String... args) {
            // TODO Auto-generated method stub
            // Check for success tag
            String username = user.getText().toString();
            String password = pass.getText().toString();
            try {
                // Building Parameters
                JSONObject data = new JSONObject();

                data.put("username", username);
                data.put("password", password);
                data.put("email", "ingvcueva@gmail.com");
                data.put("firstName", "Victor");
                data.put("lastName", "Cueva");

                File file = new File(archivoSalida);
                String encodedFile= "";
                try {
                    InputStream inputStream = null;
                    inputStream = new FileInputStream(file.getAbsolutePath());

                    byte[] buffer = new byte[10240];//specify the size to allow
                    int bytesRead;
                    ByteArrayOutputStream output = new ByteArrayOutputStream();
                    Base64OutputStream output64 = new Base64OutputStream(output, android.util.Base64.DEFAULT);

                    while ((bytesRead = inputStream.read(buffer)) != -1) {
                        output64.write(buffer, 0, bytesRead);
                    }
                    output64.close();
                    encodedFile =  output.toString();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                data.put("audio", encodedFile);

                //Posting user data to script
                JSONObject json = JSONParser.getJSONFromUrl(REGISTER_URL, "POST", data.toString());

                // full json response
                Log.d("Registering attempt", json.toString());

                // json success element
                String success;
                success = json.getString(TAG_MESSAGE);
                if (success.equals("OK")) {
                    Log.d("User Created!", json.toString());
                    finish();
                    return json.getString(TAG_MESSAGE);
                } else {
                    Log.d("Registering Failure!", json.getString(TAG_MESSAGE));
                    return json.getString(TAG_MESSAGE);
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }

            return null;
        }

        protected void onPostExecute(String file_url) {
            // dismiss the dialog once product deleted
            pDialog.dismiss();
            if (file_url != null) {
                Toast.makeText(Register.this, file_url, Toast.LENGTH_LONG).show();
            }
        }
    }

    public void Recorder(View view) {
        if (grabacion == null) {
            archivoSalida = Environment.getExternalStorageDirectory().getAbsolutePath() + "/Grabacion.mp3";
            grabacion = new MediaRecorder();
            grabacion.setAudioSource(MediaRecorder.AudioSource.MIC);
            grabacion.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
            grabacion.setAudioEncoder(MediaRecorder.OutputFormat.AMR_NB);
            grabacion.setOutputFile(archivoSalida);

            try {
                grabacion.prepare();
                grabacion.start();
            } catch (IOException e) {
                e.printStackTrace();
            }
            btn_recorder.setBackgroundResource(R.drawable.rec);
            Toast.makeText(getApplicationContext(), "Grabando...", Toast.LENGTH_SHORT).show();
        } else {
            grabacion.stop();
            grabacion.release();
            grabacion = null;
            btn_recorder.setBackgroundResource(R.drawable.stop_rec);
            Toast.makeText(getApplicationContext(), "Grabación finalizada", Toast.LENGTH_SHORT).show();
        }
    }

    public void reproducir(View view) {
        MediaPlayer mediaPlayer = new MediaPlayer();
        try {
            mediaPlayer.setDataSource(archivoSalida);
            mediaPlayer.prepare();
        } catch (IOException e) {
            e.printStackTrace();
        }
        mediaPlayer.start();
        Toast.makeText(getApplicationContext(), "Reproduciendo audio.", Toast.LENGTH_SHORT).show();
    }
}

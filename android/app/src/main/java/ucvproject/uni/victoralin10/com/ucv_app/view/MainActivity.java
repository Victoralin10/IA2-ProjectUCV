package ucvproject.uni.victoralin10.com.ucv_app.view;

import android.Manifest;
import android.app.ProgressDialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.preference.PreferenceManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Base64OutputStream;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
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

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    private EditText user, pass;
    private Button mSubmit, mRegister;

    private ProgressDialog pDialog;
    private MediaRecorder grabacion, aux;
    private String archivoSalida = null;
    private Button btn_recorder;
    private Button btn_play;

    private static final String LOGIN_URL = "https://0n31isnqy6.execute-api.us-east-1.amazonaws.com/prod/login";

    // La respuesta del JSON es
    private static final String TAG_SUCCESS = "success";
    private static final String TAG_MESSAGE = "message";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.RECORD_AUDIO}, 1000);
        }

        // setup input fields
        user = (EditText) findViewById(R.id.username);
        pass = (EditText) findViewById(R.id.password);

        // setup buttons
        btn_recorder = (Button)findViewById(R.id.btn_rec);
        btn_play = (Button)findViewById(R.id.btn_play);
        mSubmit = (Button) findViewById(R.id.login);
        mRegister = (Button) findViewById(R.id.register);

        // register listeners
        mSubmit.setOnClickListener(this);
        mRegister.setOnClickListener(this);
        btn_recorder.setOnClickListener(this);
        btn_play.setOnClickListener(this);

        archivoSalida = null;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onClick(View v) {
        // TODO Auto-generated method stub
        switch (v.getId()) {
            case R.id.login:
                if(aux == null){
                    Toast.makeText(getApplicationContext(), "Aún no graba un audio.", Toast.LENGTH_SHORT).show();
                    break;
                }
                else if(user == null || pass == null){
                    Toast.makeText(getApplicationContext(), "Username o Password sin llenar.", Toast.LENGTH_SHORT).show();
                    break;
                }
                new AttemptLogin().execute();
                break;
            case R.id.register:
                Intent i = new Intent(this, Register.class);
                startActivity(i);
                break;
            case R.id.btn_rec:
                Recorder(v);
                break;
            case R.id.btn_play:
                reproducir(v);
                break;
            default:
                break;
        }
    }

    class AttemptLogin extends AsyncTask<String, String, String> {
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            pDialog = new ProgressDialog(MainActivity.this);
            pDialog.setMessage("Attempting login...");
            pDialog.setIndeterminate(false);
            pDialog.setCancelable(true);
            pDialog.show();
        }

        @Override
        protected String doInBackground(String... args) {
            String username = user.getText().toString();
            String password = pass.getText().toString();
            try {
                // Building Parameters
                JSONObject data = new JSONObject();
                data.put("username", username);
                data.put("password", password);

                //archivoSalida
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


                Log.d("request!", "starting");
                // getting product details by making HTTP request
                JSONObject json = JSONParser.getJSONFromUrl(LOGIN_URL, "POST", data.toString());

                // check your log for json response
                Log.d("Login attempt", json.toString());

                // json success tag
                String success = json.getString(TAG_MESSAGE);
                if (success.equals("OK")) {
                    Log.d("Login Successful!", json.toString());
                    // save user data
                    SharedPreferences sp = PreferenceManager
                            .getDefaultSharedPreferences(MainActivity.this);
                    SharedPreferences.Editor edit = sp.edit();
                    edit.putString("username", username);
                    edit.apply();

                    Intent i = new Intent(MainActivity.this, ReadComments.class);
                    finish();
                    startActivity(i);
                    return json.getString(TAG_MESSAGE);
                } else {
                    Log.d("Login Failure!", json.getString(TAG_MESSAGE));
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
                Toast.makeText(MainActivity.this, file_url, Toast.LENGTH_LONG).show();
            }
        }
    }

    public void Recorder(View view){
        if(grabacion == null){
            archivoSalida = Environment.getExternalStorageDirectory().getAbsolutePath() + "/Grabacion.mp3";
            grabacion = new MediaRecorder();
            grabacion.setAudioSource(MediaRecorder.AudioSource.MIC);
            grabacion.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
            grabacion.setAudioEncoder(MediaRecorder.OutputFormat.AMR_NB);
            grabacion.setOutputFile(archivoSalida);

            try{
                grabacion.prepare();
                grabacion.start();
            }catch(IOException e){
                e.printStackTrace();
            }
            btn_recorder.setBackgroundResource(R.drawable.rec);
            Toast.makeText(getApplicationContext(), "Grabando...", Toast.LENGTH_SHORT).show();
        } else {
            grabacion.stop();
            grabacion.release();
            aux = grabacion;
            grabacion = null;
            btn_recorder.setBackgroundResource(R.drawable.stop_rec);
            Toast.makeText(getApplicationContext(), "Grabación finalizada", Toast.LENGTH_SHORT).show();
        }
    }
    public void reproducir(View view){
        MediaPlayer mediaPlayer = new MediaPlayer();
        try{
            mediaPlayer.setDataSource(archivoSalida);
            mediaPlayer.prepare();
        }catch(IOException e){
            e.printStackTrace();
        }
        mediaPlayer.start();
        Toast.makeText(getApplicationContext(), "Reproduciendo audio.", Toast.LENGTH_SHORT).show();

    }

    public void enviar(View view){
        Toast.makeText(getApplicationContext(), "Audio enviado.", Toast.LENGTH_SHORT).show();
    }
}

package ucvproject.uni.victoralin10.com.ucv_app.view;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;

import ucvproject.uni.victoralin10.com.ucv_app.R;

public class ReadComments extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // note that use read_comments.xml instead of our single_post.xml
        setContentView(R.layout.read_comments);
    }
}
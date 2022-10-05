package myproject;

import com.pulumi.Pulumi;
import com.pulumi.core.Output;
import com.pulumi.gcp.storage.Bucket;
import com.pulumi.gcp.storage.BucketArgs;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;


public class App {

    public static void main(String[] args) {
        Pulumi.run(ctx -> {
            var bucket = new Bucket("my-bucket",
                                    BucketArgs.builder()
                                    .location("US")
                                    .build());
            var strVar = "foo";
            //var arrVar = new String[]{ "fizz", "buzz" };

            ctx.export("bucketName", bucket.url());

            try {
                var readme = Files.readString(Paths.get("./Pulumi.README.md"));
                ctx.export("strVar", Output.of(strVar));
                //ctx.export("arrVar", Output.of(arrVar));
                ctx.export("readme", Output.of(readme));
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

        });

    }
}

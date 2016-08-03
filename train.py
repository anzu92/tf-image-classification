import tensorflow as tf
import config
import model
import input
import eval

FLAGS = tf.app.flags.FLAGS

def train():
    x_data, y_data = input.get_data()

    with tf.name_scope('input'):
        x = tf.placeholder("float", [None, FLAGS.height * FLAGS.width * FLAGS.depth], name='x-input')
        y = tf.placeholder("float", [None, FLAGS.num_class], name='y-input')

    hypothesis, cross_entropy, train_step = model.make_network(x, y)

    sess = tf.Session()
    merged = tf.merge_all_summaries()
    train_writer = tf.train.SummaryWriter(FLAGS.train_summary_dir, sess.graph)
    saver = tf.train.Saver()

    if tf.gfile.Exists(FLAGS.checkpoint_dir + '/model.ckpt'):
        saver.restore(sess, FLAGS.checkpoint_dir + '/model.ckpt')
    else:
        init = tf.initialize_all_variables()
        sess.run(init)

    min = 0
    max = FLAGS.batch_size

    for step in range(FLAGS.max_steps):
        summary, _ = sess.run([merged, train_step], feed_dict={x: x_data[min:max], y: y_data[min:max]})
        train_writer.add_summary(summary, step)
        print step, sess.run(cross_entropy, feed_dict={x: x_data, y: y_data})
        min += FLAGS.batch_size
        max += FLAGS.batch_size
        if (max > FLAGS.num_samples):
            min = 0
            max = FLAGS.batch_size

        if step % 100 == 0 or (step + 1) == FLAGS.max_steps:
            saver.save(sess, FLAGS.checkpoint_dir + '/model.ckpt')

def main(argv = None):
    if tf.gfile.Exists(FLAGS.train_summary_dir):
        tf.gfile.DeleteRecursively(FLAGS.train_summary_dir)
    tf.gfile.MakeDirs(FLAGS.train_summary_dir)

    if tf.gfile.Exists(FLAGS.checkpoint_dir) == False:
        tf.gfile.MakeDirs(FLAGS.checkpoint_dir)

    train()

if __name__ == '__main__':
    tf.app.run()